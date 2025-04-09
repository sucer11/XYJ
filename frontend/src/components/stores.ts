import { writable } from 'svelte/store';

export const mailCount = writable(0);
export const currentMail = writable(null);
export const selectedCategory = writable("");