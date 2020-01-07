// Auto-Focus-Cpp.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <stdio.h>
#include <tchar.h>
#include "opencv2/core.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/videoio.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int main()
{
	cout << "Built with OpenCV " << CV_VERSION << endl;
	Mat image = imread("./tmp1060.jpg");//见注1 
	/*print height and depth*/
	//imshow("img", image);//见注2//
	//resize(image, image, Size(360, 202));//见注3
	//imwrite("D:\\xinyuan.jpg", image);//见注4
	//imshow("缩小图像", image);
	//cvtColor(image, image, CV_RGB2GRAY);//见注5
	//imshow("灰度图像", image);
	//waitKey(0);//见注6

}
