# aws-lambda-exif-reader

[![Build Status](https://travis-ci.com/milancermak/aws-lambda-exif-reader.svg?token=2wCqMjFheZL9UoUpmNnQ&branch=master)](https://travis-ci.com/milancermak/aws-lambda-exif-reader)

An AWS serverless application that extracts EXIF data from images (and any other documents containing EXIF data) and stores it in a DynamoDB table for easy access. If the input file is geo-tagged, the application stores the latitude and longitude data into a secondary geo table, enabling easy geospacial queries. This allows for finding images within a certain distance from a point or in a rectangular area of interest.

You can use the `dynamo-db` geo libraries (available as an official [Java version](https://github.com/amazon-archives/dynamodb-geo) and an unofficial [JS version](https://github.com/rh389/dynamodb-geo.js)) to perform the geospatial queries.

The app is [available](https://serverlessrepo.aws.amazon.com/#/applications/arn:aws:serverlessrepo:us-east-1:790194644437:applications~exif-reader) in the AWS Serverless repository.
