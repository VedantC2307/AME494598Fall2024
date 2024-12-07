#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // Replace with your phone's IP address and port from IP Webcam app
    std::string rtsp_url = "rtsp://192.168.0.161:8080/h264_ulaw.sdp";
    
    // Open the RTSP stream
    cv::VideoCapture cap(rtsp_url);
    
    if (!cap.isOpened()) {
        std::cerr << "Error: Unable to open the RTSP stream!" << std::endl;
        return -1;
    }

    cv::Mat frame;
    
    while (true) {
        // Capture frame-by-frame
        cap >> frame;
        
        // Check if the frame is empty
        if (frame.empty()) {
            std::cerr << "Error: Empty frame!" << std::endl;
            break;
        }

        // Display the resulting frame
        cv::imshow("Phone Camera Stream", frame);
        
        // Press 'q' to exit the loop
        if (cv::waitKey(1) == 'q') {
            break;
        }
    }

    // Release the video capture object
    cap.release();
    cv::destroyAllWindows();

    return 0;
}
