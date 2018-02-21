const std::string url = “http://192.168.3.25:1935/live/myStream/playlist.m3u8";

cv::VideoCapture capture(url);

if (!capture->isOpened()) {
    //Error
}

cv::namedWindow("Stream", CV_WINDOW_AUTOSIZE);

cv::Mat frame;

while(stream_enable) {
    if (!capture->read(frame)) {
        //Error
    }
    cv::imshow("Stream", frame);

    cv::waitKey(30);
}
