import React from 'react';

/**
 * Guest Table Component - Displays RSVP guest list
 */
export default function GuestTable({ rsvps, t }) {
    return (
        <div className="table-responsive">
            <table className="rsvp-table">
                <thead>
                    <tr>
                        <th>{t.name}</th>
                        <th>{t.status}</th>
                        <th>{t.guests}</th>
                        <th>{t.total}</th>
                    </tr>
                </thead>
                <tbody>
                    {rsvps.map((r, i) => (
                        <tr key={i}>
                            <td>{r.name} <span style={{ fontSize: '0.8em', color: '#666' }}>({r.email})</span></td>
                            <td>
                                <span className={`status-badge ${r.status}`}>
                                    {r.status === 'attending' ? t.statusAttending :
                                        r.status === 'pending' ? t.statusPending :
                                            r.status === 'not_attending' ? t.statusNotAttending : r.status}
                                </span>
                            </td>
                            <td>{r.guests_count}</td>
                            <td>
                                {r.status === 'attending' ? (1 + (r.guests_count || 0)) : '-'}
                            </td>
                        </tr>
                    ))}
                    {rsvps.length === 0 && (
                        <tr>
                            <td colSpan="4" style={{ textAlign: 'center' }}>{t.noGuests}</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
    );
}
