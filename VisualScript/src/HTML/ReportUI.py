
def getTitle(title):
    htmlHead = r"""
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!-- <link rel="icon" href="/static/favicon.png?v=2" type="image/x-icon" /> -->
  <title>""" + str(title) + """ Report</title>
  <!-- Bootstrap -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/bootstrap/3.3.6/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/fancybox/2.1.5/jquery.fancybox.min.css">
  <!--
  <link rel="stylesheet" href="http://gohttp.nie.netease.com/qard-libs/libs/bootstrap/3.3.5/css/bootstrap.min.css">
  <link rel="stylesheet" href="http://gohttp.nie.netease.com/qard-libs/libs/fancybox/2.1.5/jquery.fancybox.min.css">
  <link rel="stylesheet" href="//cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
  -->
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

  span.success {
    color: white;
    background-color: green;
    padding: 3px;
  }

  span.failure {
    color: white;
    background-color: red;
    padding: 3px;
  }
  </style>
</head>

<body id="app">
  <nav class="navbar navbar-default navbar-fixed-top">
    <div class="container">
      <div class="navbar-header">
        <a class="navbar-brand">""" + str(title) + """ Report</a>
      </div>
    </div>
  </nav>
"""
    return htmlHead
