import fs from 'fs';
import env from '../env';
import engineApi from '../api/engineApi';

const getWavFileName = () => {
  const currentDate = new Date();

  const year = String(currentDate.getFullYear());
  const month = String(currentDate.getMonth() + 1).padStart(2, 0);
  const date = String(currentDate.getDate()).padStart(2, 0);
  const hours = String(currentDate.getHours()).padStart(2, 0);
  const minutes = String(currentDate.getMinutes()).padStart(2, 0);
  const seconds = String(currentDate.getSeconds()).padStart(2, 0);
  const milliSeconds = String(currentDate.getMilliseconds()).padStart(3, 0);

  const fileName = `${year}${month}${date}${hours}${minutes}${seconds}${milliSeconds}.wav`;
  return {
    path: `${env.AUDIO_BASE_DIR}/${fileName}`,
    fileName,
  };
};

const calcVoice = async (charId, wavBinary) => {
  const { path, fileName } = getWavFileName();
  fs.writeFileSync(path, wavBinary);

  // エンジンにぶん投げる
  try {
    const { score } = await engineApi.getVoiceScore(charId, `${env.APP_BASE_URL}/${fileName}`);
    return score;
  } catch (e) {
    throw new Error(e);
  }
};

export default {
  calcVoice,
};
