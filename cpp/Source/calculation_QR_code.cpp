// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Calculation on QR Code
******************************************************************************/

#include "..\Header\calculation_QR_code.h"

//Read img name to scan the QR code inside
int ReadQRCode(Mat inputImage) {

	if (!inputImage.data) {

		cout << "Could not open or find the image" << endl;
		return -1;
	}
	// initialization
	QRCodeDetector qrDecoder = QRCodeDetector::QRCodeDetector();
	vector<Point> points;

	// detect and recognize QR code
	string data = qrDecoder.detectAndDecode(inputImage, points);

	if (data.length() > 0){

		// content of detected QR code
		cout << "Decoded Data: \n\n" << data << endl;

		// draw bouding box around QR code 
		//rectangle(inputImage, points[0], points[2], Scalar(0, 255, 0), 2);
		line(inputImage, points[0], points[1], Scalar(0, 255, 0), 2);
		line(inputImage, points[1], points[2], Scalar(0, 255, 0), 2);
		line(inputImage, points[2], points[3], Scalar(0, 255, 0), 2);
		line(inputImage, points[3], points[0], Scalar(0, 255, 0), 2);
	}
	else{

		cout << "WARNING: QR Code not detected" << endl;
	}
	namedWindow("Detected QR Code", 0);
	resizeWindow("Detected QR Code", 640, 480);
	imshow("Detected QR Code", inputImage);

	waitKey(0);

	return 0;
}