const AUDIO_BASE_DIR = process.env.AUDIO_BASE_DIR || 'audio';
const APP_BASE_URL = process.env.APP_BASE_URL || 'localhost:3001';
const { ENGINE_BASE_URL } = process.env;

export default {
  AUDIO_BASE_DIR,
  APP_BASE_URL,
  ENGINE_BASE_URL,
};
