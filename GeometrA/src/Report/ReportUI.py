
def getTitle(title):
    htmlHead = r'''<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>''' + str(title) + ''' Report</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/bootstrap/3.3.6/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/fancybox/2.1.5/jquery.fancybox.min.css">


  <style>
    body {
      padding-top: 70px;
    }

    .info-name {
      padding-right: 1em;
      display: inline-block;
      width: 7em;
      font-family: 'Courier New';
      font-weight: 700;
    }

    ul.device-info {
      padding-left: 10px;
    }

    ul.device-info > li {
      list-style-type: none;
    }

    div.image-wrapper {
      position: relative;
      overflow: hidden;
      max-width: 300px;
      margin: 0 auto;
    }

    .image-wrapper > img {
      border: 1px solid black;
    }

    span.positioner {
      position: absolute;
      display: block;
    }

    span.finger {
      position: absolute;
      display: block;
      border-radius: 50%;
      width: 8mm;
      height: 8mm;
      top: -4mm;
      left: -4mm;
      pointer-events: none;
      border-width: 1px;
      border-color: #464646;
      opacity: 0.5;
      background-color: red;
    }

    .halfsize {
      -moz-transform: scale(0.5);
      -webkit-transform: scale(0.5);
      transform: scale(0.5);
    }

    a.anchor {
      display: block;
      position: relative;
      top: -70px;
      visibility: hidden;
      width: 0px;
      height: 0px;
    }

    .btn {
      border-radius: 5px;
      padding: 15px 25px;
      font-size: 22px;
      text-decoration: none;
      margin: 20px;
      color: #fff;
      position: absolute;
      display: inline-block;
      align-content: center;

    }

    .btn:active {
      transform: translate(0px, 5px);
      -webkit-transform: translate(0px, 5px);
      box-shadow: 0px 1px 0px 0px;
    }

    .blue {
      background-color: #55acee;
      box-shadow: 0px 5px 0px 0px #3C93D5;
    }

    .blue:hover {
      background-color: #6FC6FF;
    }
  </style>
</head>
<body id="app">
  <!-- Header  -->
  <nav class="navbar navbar-default navbar-fixed-top">
    <div class="container">
      <div class="navbar-header">
        <a class="navbar-brand">Test 1</a>
      </div>
    </div>
  </nav>
'''
    return htmlHead
