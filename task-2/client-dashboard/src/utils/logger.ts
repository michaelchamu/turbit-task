
declare const process: {
    env: {
        NODE_ENV: string;
    };
};

import pino from 'pino';

const logger = pino({
    browser: {
        asObject: true,
    },
    level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
    ...(process.env.NODE_ENV !== 'production' && {
        transport: {
            target: 'pino-pretty',
            options: {
                colorize: true,
                translateTime: 'HH:MM:ss',
            },
        },
    }),
});

export default logger;