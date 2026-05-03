exports.handler = (event, context, callback) => {
  const headers = event.headers || {};
  const auth = headers.Authorization || headers.authorization || null;

  let req;
  try {
    req = JSON.parse(event.body);
  } catch {
    return callback(null, {
      statusCode: 400,
      body: JSON.stringify({ status: "err", message: "Invalid JSON" })
    });
  }

  const auth_header = headers.Authorization || headers.authorization;
  const token_sections = auth_header.split('.');
  // ... decode JWT and continue safely
};
