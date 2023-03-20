const ytdl = require("ytdl-core");

exports.handler = async function (event) {
  try {
    let bodyJSON = JSON.parse(event.body);
    const info = await ytdl.getInfo(bodyJSON.data.url);
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
        message: "Không tìm thấy video mà bạn yêu cầu.",
      }),
    };
  }
};
