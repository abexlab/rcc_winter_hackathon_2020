import express from 'express';
import bodyParser from 'body-parser';
import rankController from './controller/rankController';
import voiceController from './controller/voiceController';
import errorController from './controller/errorController';

const start = () => {
  const app = express();

  app.get('/rank/:char_id', (req, res) => {
    const charId = Number(req.params.char_id);
    res.json(rankController.getRankByCharId(charId));
  });

  app.use(bodyParser.raw({
    type: 'audio/wav',
  }));

  app.post('/voice/calc/:char_id', (req, res) => {
    const contentType = req.headers['content-type'];

    if (contentType !== 'audio/wav') {
      errorController.returnBadRequest(res, 'Content-Type is invalid.');
      return;
    }

    const charId = Number(req.params.char_id);
    const wavBinary = req.body;
    voiceController.calcVoice(charId, wavBinary)
      .then((score) => {
        res.json({
          score,
        });
      })
      .catch(() => {
        errorController.returnUnexpectedError(res, 'Unexpected error.');
      });
  });

  // サーバ起動
  app.listen(3000, () => {
    // eslint-disable-next-line no-console
    console.log('Server started on 3000.');
  });
};

export default {
  start,
};
