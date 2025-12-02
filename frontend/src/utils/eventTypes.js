// Event types configuration with Hebrew translations and background images

const EVENT_TYPES = {
    wedding: {
        en: 'Wedding',
        he: 'חתונה',
        backgrounds: ['wadding.jpg', 'wadding2.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1519751138087-5bf79df62d58?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    henna: {
        en: 'Henna',
        he: 'חינה',
        backgrounds: ['Henna.jpg', 'Henna1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1596238846747-380d46b07d6c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    engagement: {
        en: 'Engagement',
        he: 'אירוסין',
        backgrounds: ['Engagement.jpg', 'Engagement1.jpg', 'Engagement2.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1515934751635-c81c6bc9a2d8?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    bar_mitzvah: {
        en: 'Bar Mitzvah',
        he: 'בר מצווה',
        backgrounds: ['bar_miztvah.jpg', 'bar_miztvah1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1587271407850-8d43891882c7?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    bat_mitzvah: {
        en: 'Bat Mitzvah',
        he: 'בת מצווה',
        backgrounds: ['bat_miztvah.jpg', 'bat_miztvah1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1530103862676-de3c9a59af57?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    brit_milah: {
        en: 'Brit Milah',
        he: 'ברית מילה',
        backgrounds: ['brita_mila.jpg', 'brita_mila1.jpg', 'brita_mila2.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1519689680058-324335c77eba?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    brit_bat: {
        en: 'Brit Bat',
        he: 'בריתה',
        backgrounds: ['brita.jpg', 'brita1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1519689680058-324335c77eba?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    birthday: {
        en: 'Birthday',
        he: 'ימי הולדת',
        backgrounds: ['B_day.jpg', 'B_day1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1464349153912-656365a98b46?ixlib=rb-4.0.3&auto=format&fit=crop&w=2074&q=80'
    },
    shabbat_hatan: {
        en: 'Shabbat Hatan',
        he: 'שבת חתן',
        backgrounds: ['Shabbat_Hatan.jpg', 'Shabbat_Hatan1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1528605248644-14dd04022da1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    bachelor_party: {
        en: 'Bachelor/Bachelorette Party',
        he: 'מסיבת רווקים/רווקות',
        backgrounds: ['Bachelor-bachelorette_party.jpg', 'Bachelor-bachelorette_party1.jpg', 'Bachelor-bachelorette_party2.jpg', 'Bachelor-bachelorette_party3.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    corporate: {
        en: 'Corporate Events',
        he: 'אירועי חברה',
        backgrounds: ['corporate_conferences.jpg', 'corporate_conferences1.jpg', 'tech_innovation.jpg', 'tech_innovation1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1511578314322-379afb476865?ixlib=rb-4.0.3&auto=format&fit=crop&w=2069&q=80'
    },
    conference: {
        en: 'Conference',
        he: 'כנסים',
        backgrounds: ['corporate_conferences.jpg', 'corporate_conferences1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1544531586-fde5298cdd40?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    graduation: {
        en: 'Graduation',
        he: 'טקסי סיום',
        backgrounds: ['graduation.jpg', 'graduation1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    prom: {
        en: 'Prom',
        he: 'נשף סיום',
        backgrounds: ['prom.jpg', 'prom1.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1519750157634-b6d493a0f77c?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
    },
    party: {
        en: 'Party',
        he: 'מסיבות',
        backgrounds: ['party.jpg', 'party1.jpg', 'party2.jpg', 'party3.jpg', 'party4.jpg', 'party5.jpg', 'party6.jpg', 'party7.jpg'],
        emailBackground: 'https://images.unsplash.com/photo-1530103862676-de3c9a59af57?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80'
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
    return backgrounds[randomIndex];
};

// Get all backgrounds for event type
export const getBackgrounds = (type) => {
    return EVENT_TYPES[type]?.backgrounds || [];
};

// Get email background (Unsplash URL) for event type
export const getEmailBackground = (type) => {
    return EVENT_TYPES[type]?.emailBackground || EVENT_TYPES['wedding'].emailBackground;
};

export default EVENT_TYPES;
