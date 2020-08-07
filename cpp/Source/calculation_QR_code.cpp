// -*- coding: utf-8 -*-
/******************************************************************************
@author: Wei Huajing
@company: KAMERAWERK
@e-mail: jerryweihuajing@126.com

@title: Source-Calculation on QR Code
******************************************************************************/

#include "..\Header\calculation_QR_code.h"

//Read img name to scan the QR code inside
int ReadQRCode(Mat img_QR_code) {

	if (!img_QR_code.data) {

		cout << "Could not open or find the image" << endl;
		return -1;
	}
	// initialization
	QRCodeDetector qrDecoder = QRCodeDetector::QRCodeDetector();
	vector<Point> points;

	// detect and recognize QR code
	string data = qrDecoder.detectAndDecode(img_QR_code, points);

	if (data.length() > 0){

		// content of detected QR code
		cout << "Decoded Data: \n\n" << data << endl;

		// draw bouding box around QR code 
		rectangle(img_QR_code, points[0], points[2], Scalar(0, 255, 0), 2);
		imshow("Detected QR Code", img_QR_code);

		waitKey(0);
	}
	else{

		cout << "WARNING: QR Code not detected" << endl;
	}
	return 0;
}