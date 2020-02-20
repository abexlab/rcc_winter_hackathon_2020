const getRankByCharId = (charId) => {
  const result = {
    char_id: charId,
    ranks: [
      {
        rank: 1,
        name: '一般男性1',
        score: 97.65,
      },
      {
        rank: 2,
        name: '一般男性2',
        score: 97.65,
      },
      {
        rank: 3,
        name: '一般男性3',
        score: 97.65,
      },
    ],
  };
  return result;
};

export default {
  getRankByCharId,
};
