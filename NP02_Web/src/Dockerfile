# Please move this to the root of the project to run Docker

FROM ubuntu:16.04

# Install dependencies
EXPOSE 8080

# Copy source code
COPY src/public/ /app/web
COPY exe/ /app/main

# Run the server
CMD ["./app/main/main"]