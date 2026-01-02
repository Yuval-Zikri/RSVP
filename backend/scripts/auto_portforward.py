#!/usr/bin/env python3
"""
auto_portforward.py

Watches for pod start events and ensures `kubectl port-forward` is running
for the Prometheus and Grafana services. Meant to be run from a developer
machine with `kubectl` configured (or in-cluster if desired).

Environment variables / args:
- SERVICE_NAMESPACE: namespace where the `prometheus` and `grafana` services live (default: "default")

Usage:
  python backend/scripts/auto_portforward.py

Dependencies: `kubernetes` Python client and `kubectl` in PATH.
"""

import os
import signal
import shutil
import subprocess
import sys
import threading
import time
from typing import Dict, Optional

try:
    from kubernetes import client, config, watch
except Exception as e:
    print("Missing dependency 'kubernetes'. Install with: pip install kubernetes", file=sys.stderr)
    raise


SERVICE_NAMESPACE = os.environ.get("SERVICE_NAMESPACE", "default")
PORTFORWARDS = [
    ("prometheus", "9090:9090"),
    ("grafana", "3000:3000"),
]

_procs: Dict[str, subprocess.Popen] = {}
_stop = threading.Event()


def check_kubectl() -> None:
    if shutil.which("kubectl") is None:
        print("kubectl not found in PATH. Please install/configure kubectl.", file=sys.stderr)
        sys.exit(2)


def start_portforward(svc_name: str, port_map: str, namespace: str) -> subprocess.Popen:
    args = [
        "kubectl",
        "port-forward",
        f"svc/{svc_name}",
        port_map,
        "-n",
        namespace,
    ]
    # Keep the subprocess attached so it runs until explicitly stopped.
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p


def ensure_portforwards(namespace: str) -> None:
    for svc, mapping in PORTFORWARDS:
        p = _procs.get(svc)
        if p is None or p.poll() is not None:
            if p is not None:
                try:
                    p.kill()
                except Exception:
                    pass
            print(f"Starting port-forward for {svc} -> {mapping} (namespace={namespace})")
            _procs[svc] = start_portforward(svc, mapping, namespace)


def monitor_procs(namespace: str, interval: float = 5.0) -> None:
    while not _stop.is_set():
        for svc in list(_procs.keys()):
            p = _procs.get(svc)
            if p is None:
                continue
            if p.poll() is not None:
                print(f"Port-forward for {svc} exited; restarting")
                _procs[svc] = start_portforward(svc, dict(PORTFORWARDS)[svc], namespace)  # type: ignore
        time.sleep(interval)


def shutdown(signum: Optional[int] = None, frame: Optional[object] = None) -> None:
    _stop.set()
    print("Shutting down port-forward processes...")
    for svc, p in _procs.items():
        try:
            p.terminate()
        except Exception:
            pass
    # Give processes a moment
    time.sleep(0.5)
    for svc, p in _procs.items():
        if p.poll() is None:
            try:
                p.kill()
            except Exception:
                pass
    sys.exit(0)


def main() -> None:
    check_kubectl()

    # Load kube config (works for both local kubeconfig and in-cluster)
    try:
        config.load_kube_config()
    except Exception:
        try:
            config.load_incluster_config()
        except Exception as e:
            print("Could not configure Kubernetes client:\n", e, file=sys.stderr)
            sys.exit(1)

    v1 = client.CoreV1Api()
    w = watch.Watch()

    # Start monitoring thread for port-forward processes
    monitor_thread = threading.Thread(target=monitor_procs, args=(SERVICE_NAMESPACE,), daemon=True)
    monitor_thread.start()

    # Ensure port-forwards are running at startup if any pod is already running
    try:
        pods = v1.list_pod_for_all_namespaces(limit=1)
        if pods and pods.items:
            ensure_portforwards(SERVICE_NAMESPACE)
    except Exception:
        # ignore startup check failures; the watch below will trigger on new pods
        pass

    print("Watching for pod start events. Press Ctrl-C to stop.")

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        for event in w.stream(v1.list_pod_for_all_namespaces, timeout_seconds=0):
            if _stop.is_set():
                break
            typ = event.get('type')
            pod = event.get('object')
            if not pod:
                continue
            phase = getattr(pod.status, 'phase', None)
            if typ in ("ADDED", "MODIFIED") and phase == "Running":
                # A pod has started/running; ensure our port-forwards are active.
                ensure_portforwards(SERVICE_NAMESPACE)
    except Exception as e:
        if not _stop.is_set():
            print("Watcher error:", e, file=sys.stderr)
    finally:
        shutdown()


if __name__ == "__main__":
    main()
