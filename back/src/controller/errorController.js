const returnBadRequest = (res, message) => {
  res.status = 400;
  res.json({
    error: message,
  });
};

const returnUnexpectedError = (res, message) => {
  res.status = 500;
  res.json({
    error: message,
  });
};

export default {
  returnBadRequest,
  returnUnexpectedError,
};
