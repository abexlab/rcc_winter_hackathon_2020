import axios from 'axios';
import env from '../env';

const getVoiceScore = async (charId, url) => {
  if (!env.ENGINE_BASE_URL) {
    return {
      score: 20.34,
    };
  }

  const params = {
    char_id: charId,
    url,
  };

  try {
    const res = await axios.get(`${env.ENGINE_BASE_URL}/voice/calc`, {
      params,
    });
    return res.data;
  } catch (e) {
    // eslint-disable-next-line no-console
    console.log('Engineとの通信に失敗しました');
    throw new Error(e);
  }
};

export default {
  getVoiceScore,
};
