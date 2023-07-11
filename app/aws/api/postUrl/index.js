const dotenv = require("dotenv");
const AWS = require("aws-sdk");
const TableName = "URLShortener";

// AWS configuration
dotenv.config();
const { MY_AWS_ACCESS_KEY_ID, MY_AWS_SECRET_ACCESS_KEY, MY_AWS_REGION } =
  process.env;
AWS.config.update({
  credentials: {
    accessKeyId: MY_AWS_ACCESS_KEY_ID,
    secretAccessKey: MY_AWS_SECRET_ACCESS_KEY,
  },
  region: MY_AWS_REGION,
});
var dynamodb = new AWS.DynamoDB({ apiVersion: "2012-08-10" });

// Check if the URL is valid
const stringIsAValidUrl = (string) => {
  const pattern = new RegExp(
    "^(https?:\\/\\/)?" + // protocol
    "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
    "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
    "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
    "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
    "(\\#[-a-z\\d_]*)?$", // fragment locator
    "i"
  );
  return pattern.test(string);
};

exports.handler = async function (event) {
  // Expose body
  let body = JSON.parse(event.body);

  // Handle POST request
  if (event.httpMethod == "POST") {
    var longURL = body.data.url;

    // Check if the URL is valid
    if (stringIsAValidUrl(longURL) &&
      ((longURL.startsWith("http://") || longURL.startsWith("https://")))) {
      var status, message;

      // Check if the URL is already shorten
      if (longURL.includes("https://api.builetuananh.name.vn")) {
        return {
          statusCode: 400,
          body: JSON.stringify({
            status: 400,
            message: "Đường dẫn này đã được rút gọn.",
          }),
        };
      }

      // Shorten the URL
      else {
        status = 200;
        var response = await dynamodb
          .scan({
            FilterExpression: "longURL = :longURL",
            ExpressionAttributeValues: {
              ":longURL": {
                S: longURL,
              },
            },
            TableName: TableName,
          })
          .promise();

        if (response.Count == 0) {
          var shortURL =
            "https://api.builetuananh.name.vn/" + Date.now().toString(36);
          var parameters = {
            TableName: TableName,
            Item: { longURL: { S: longURL }, shortURL: { S: shortURL } },
          };
          await dynamodb.putItem(parameters).promise();
        } else {
          shortURL = response.Items[0].shortURL["S"];
        }
        message = shortURL;
      }
      return {
        statusCode: status,
        body: JSON.stringify({
          status: status,
          message: message,
        }),
      };
    }

    // If the URL is not valid
    else
      return {
        statusCode: 404,
        body: JSON.stringify({
          status: 404,
          message: "Đường dẫn không hợp lệ. Vui lòng kiểm tra lại.",
        }),
      };
  }

  // Handle other request
  else
    return {
      statusCode: 400,
      body: JSON.stringify({
        status: 400,
        message: "Yêu cầu không hợp lệ. Vui lòng kiểm tra lại.",
      }),
    };
};
