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

exports.handler = async function (event) {
  try {
    var response = await dynamodb
      .scan({
        FilterExpression: "shortURL = :shortURL",
        ExpressionAttributeValues: {
          ":shortURL": {
            S: "https://api.builetuananh.name.vn" + event.path,
          },
        },
        TableName: TableName,
      })
      .promise();
    // console.log(response);
    if (response.Count == 1) {
      return {
        statusCode: 301,
        headers: {
          Location: response.Items[0].longURL["S"],
        },
      };
    } else {
      return {
        statusCode: 301,
        headers: {
          Location: "https://services.builetuananh.name.vn/404.html",
        },
      };
    }
  } catch (error) {
    return {
      statusCode: 301,
      error: error.message,
      stack: error.stack,
      headers: {
        Location: "https://services.builetuananh.name.vn/404.html",
      },
    };
  }
};
