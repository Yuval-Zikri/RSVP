// Event types configuration with Hebrew translations and background images

const EVENT_TYPES = {
    wedding: {
        en: 'Wedding',
        he: 'חתונה',
        backgrounds: ['wadding.jpg', 'wadding2.jpg']
    },
    henna: {
        en: 'Henna',
        he: 'חינה',
        backgrounds: ['Henna.jpg', 'Henna1.jpg']
    },
    engagement: {
        en: 'Engagement',
        he: 'אירוסין',
        backgrounds: ['Engagement.jpg', 'Engagement1.jpg', 'Engagement2.jpg']
    },
    bar_mitzvah: {
        en: 'Bar Mitzvah',
        he: 'בר מצווה',
        backgrounds: ['bar_miztvah.jpg', 'bar_miztvah1.jpg']
    },
    bat_mitzvah: {
        en: 'Bat Mitzvah',
        he: 'בת מצווה',
        backgrounds: ['bat_miztvah.jpg', 'bat_miztvah1.jpg']
    },
    brit_milah: {
        en: 'Brit Milah',
        he: 'ברית מילה',
        backgrounds: ['brita_mila.jpg', 'brita_mila1.jpg', 'brita_mila2.jpg']
    },
    brit_bat: {
        en: 'Brit Bat',
        he: 'בריתה',
        backgrounds: ['brita.jpg', 'brita1.jpg']
    },
    birthday: {
        en: 'Birthday',
        he: 'ימי הולדת',
        backgrounds: ['B_day.jpg', 'B_day1.jpg']
    },
    shabbat_hatan: {
        en: 'Shabbat Hatan',
        he: 'שבת חתן',
        backgrounds: ['Shabbat_Hatan.jpg', 'Shabbat_Hatan1.jpg']
    },
    bachelor_party: {
        en: 'Bachelor/Bachelorette Party',
        he: 'מסיבת רווקים/רווקות',
        backgrounds: ['Bachelor-bachelorette_party.jpg', 'Bachelor-bachelorette_party1.jpg', 'Bachelor-bachelorette_party2.jpg', 'Bachelor-bachelorette_party3.jpg']
    },
    corporate: {
        en: 'Corporate Events',
        he: 'אירועי חברה',
        backgrounds: ['corporate_conferences.jpg', 'corporate_conferences1.jpg', 'tech_innovation.jpg', 'tech_innovation1.jpg']
    },
    conference: {
        en: 'Conference',
        he: 'כנסים',
        backgrounds: ['corporate_conferences.jpg', 'corporate_conferences1.jpg']
    },
    graduation: {
        en: 'Graduation',
        he: 'טקסי סיום',
        backgrounds: ['graduation.jpg', 'graduation1.jpg']
    },
    prom: {
        en: 'Prom',
        he: 'נשף סיום',
        backgrounds: ['prom.jpg', 'prom1.jpg']
    },
    party: {
        en: 'Party',
        he: 'מסיבות',
        backgrounds: ['party.jpg', 'party1.jpg', 'party2.jpg', 'party3.jpg', 'party4.jpg', 'party5.jpg', 'party6.jpg', 'party7.jpg']
    }
};

// Get event type name based on language
export const getEventTypeName = (type, language = 'en') => {
    return EVENT_TYPES[type]?.[language] || type;
};

// Get all event types as array
export const getAllEventTypes = () => {
    return Object.keys(EVENT_TYPES);
};

// Get random background for event type
export const getRandomBackground = (type) => {
    const backgrounds = EVENT_TYPES[type]?.backgrounds || [];
    if (backgrounds.length === 0) return null;
    const randomIndex = Math.floor(Math.random() * backgrounds.length);
    // Use relative path from the component location
    return new URL(`../background/${backgrounds[randomIndex]}`, import.meta.url).href;
};

// Get all backgrounds for event type
export const getBackgrounds = (type) => {
    return EVENT_TYPES[type]?.backgrounds || [];
};

export default EVENT_TYPES;
