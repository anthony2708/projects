const ytdl = require("ytdl-core");

exports.handler = async function (event) {
  try {
    let body = JSON.parse(event.body);
    let urlToGet = body.data.url;
    const info = await ytdl.getInfo(urlToGet);
    return {
      statusCode: 200,
      body: JSON.stringify({
        url: "https://www.youtube.com/embed/" + info.videoDetails.videoId,
        title: info.videoDetails.title,
        info: info.formats.sort((a, b) => {
          return a.mimeType < b.mimeType;
        }),
      }),
    };
  } catch (error) {
    return {
      statusCode: 404,
      body: JSON.stringify({
        status: 404,
        error: error.message,
        stack: error.stack,
        message:
          "Không thể tìm thấy video mà bạn yêu cầu. Xin vui lòng thử lại",
      }),
    };
  }
};
