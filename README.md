# Project *Vector Vision*
___
Project to experiment with: Azure Vision service, Flask, html. <br>
Using robot Vector (DDL/Anki's Robot: https://www.digitaldreamlabs.com/products/vector-robot)
<br>

## Description
A web page interface allows the user to take a picture with Vector front camera of a desired scene
(image, drawing, actual scene,...). <br>
Then the picture is analyzed with *Azure Vision* service, which provide a description (caption) 
and the writen text on the picture, if any. <br>
The picture description and writen text is *voiced* by Vector. <br>

Here is a demonstration video: <br>
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/H8RSK83AzeI/0.jpg)](https://www.youtube.com/watch?v=H8RSK83AzeI)


## Helpful methods/code
Azure Vision SDK and exemples :<br> 
https://github.com/Azure-Samples/azure-ai-vision-sdk/tree/main/samples/python/image-analysis

## Current limitation / bug
Tests have been conducted only with Flask's development server <br>
  