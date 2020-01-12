// ConsoleDemo.cpp : Defining entry points for console applications。
//

#include "stdafx.h"
#include "ConsoleDemo.h"
#include <vector>
#include <opencv2\opencv.hpp>
#include<opencv2\imgproc\imgproc.hpp>
#include<opencv2\imgproc\imgproc_c.h>
#include<opencv2\highgui\highgui.hpp>
#include "..\\DTCCM2_SDK\\dtccm2.h"
#include "IniFileRW.h"
#include "..\\LC898124EP1/DownloadCmd.h"
#include "..\\LC898124EP1/HighLevelCmd.h"
#include <Eigen\Dense>

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// The only application object

CWinApp theApp;

using namespace std;
using namespace cv;
using namespace Eigen;

#pragma comment(lib,"..\\DTCCM2_SDK\\dtccm2.lib")

char*      m_pSensorName;
USHORT*    m_pSensorPara;
USHORT*    m_pSensorSleepPara;

//20130823 added..
USHORT*		m_pAF_InitParaList;
USHORT*		m_pAF_AutoParaList;
USHORT*		m_pAF_FarParaList;
USHORT*		m_pAF_NearParaList;
USHORT*		m_pExposure_ParaList;
USHORT*		m_pGain_ParaList;

	ULONG m_GrabSize = 0;
float m_fAvdd = 2.8;
float m_fDovdd = 1.8;
float m_fDvdd = 1.2;
float m_fAfvcc = 2.8;
float m_fVpp = 2.8;
float m_fMclk = 18;

BOOL	m_isTV;

//get gray value of img gray

int GetValueFromImgGray(Mat img_gray,int i,int j){

	//size of img//
	int cols = img_gray.cols;
	int rows = img_gray.rows;

	int channels = img_gray.channels();

	if (channels == 1)

	{
		//iteration from start 
		Mat_<uchar>::iterator it_begin = img_gray.begin<uchar>();

		int pixel = *(it_begin + cols * i + j);

		return pixel;
	}

}

int GetValueFromImgRGB(Mat img_bgr,int i,int j){
	
	Vec3i bgr = img_bgr.at<Vec3b>(i, j);

	int B, G, R;

	B = bgr.val[0];
	G = bgr.val[1];
	R = bgr.val[2];

	return (R * 30 + G * 59 + B * 11) / 100;
}


vector<string> split(const string &s, const string &seperator)
{
	vector<string> result;
	typedef string::size_type string_size;
	string_size i = 0;
	while (i != s.size()) {
		//Find the first letter in the string that is not equal to the separator.
		int flag = 0;
		while (i != s.size() && flag == 0)
		{
			flag = 1;
			for (string_size x = 0; x < seperator.size(); ++x)
				if (s[i] == seperator[x])
				{
					++i;
					flag = 0;
					break;
				}
		}

		//Find another delimiter to extract the string between the two separators
		flag = 0;
		string_size j = i;
		while (j != s.size() && flag == 0)
		{
			for (string_size x = 0; x < seperator.size(); ++x)
				if (s[j] == seperator[x])
				{
					flag = 1;
					break;
				}
			if (flag == 0)
				++j;
		}
		if (i != j)
		{
			result.push_back(s.substr(i, j - i));
			i = j;
		}
	}
	return result;
}

BOOL bGetI2CDataFromLibFile(CString filename, pSensorTab pSensor)
{
	CStdioFile file;
	if (!file.Open((filename), CFile::modeRead | CFile::typeText))
	{
		return FALSE;
	}
	CString szLine = _T("");
	UINT addr =0, reg=0, value=0;
	BYTE i2cmode = 0;
	USHORT *pParaList= m_pSensorPara;
	USHORT *pSleepParaList = m_pSensorSleepPara;
	USHORT *pAF_InitParaList = m_pAF_InitParaList;
	USHORT *pAF_AutoParaList = m_pAF_AutoParaList;
	USHORT *pAF_FarParaList = m_pAF_FarParaList;
	USHORT *pAF_NearParaList = m_pAF_NearParaList;
	USHORT *pExposure_ParaList = m_pExposure_ParaList;
	USHORT *pGain_ParaList = m_pGain_ParaList;

	USHORT ParaListSize=0;
	USHORT SleepParaListSize = 0;
	USHORT AF_InitParaListSize = 0;
	USHORT AF_AutoParaListSize = 0;
	USHORT AF_FarParaListSize = 0;
	USHORT AF_NearParaListSize = 0;
	USHORT Exposure_ParaListSize = 0;
	USHORT Gain_ParaListSize = 0;


	CString sReg, sVal;
	CString strTmp[10];
	int tmp = 0;
	strTmp[0] = "[ParaList]";
	strTmp[1] = "[SleepParaList]";
	strTmp[2] = "[AF_InitParaList]";
	strTmp[3] = "[AF_AutoParaList]";
	strTmp[4] = "[AF_FarParaList]";
	strTmp[5] = "[AF_NearParaList]";
	strTmp[6] = "[Exposure_ParaList]";
	strTmp[7] = "[Gain_ParaList]";

	for(int i = 0; i <10; i++)
	{
		strTmp[i].MakeLower();
		strTmp[i].Trim();
	}
	int state = -1;
	while(file.ReadString(szLine))
	{
		CString Textout;
		//寻找注释符号或者']',如果有这样的，只取前面的，
		tmp = szLine.FindOneOf("//"); 
		if( tmp == 0)
		{
			continue;
		}
		else if(tmp > 0)
		{
			szLine = szLine.Left(tmp);
		}
		tmp = szLine.FindOneOf("]"); 
		if( tmp == 0)
		{
			continue;
		}
		else if(tmp > 0)
		{
			szLine = szLine.Left(tmp+1);
		}
		szLine.MakeLower();
		szLine.TrimLeft();
		szLine.TrimRight();		

		if(szLine == strTmp[0]) 
		{
			state = 0;
			ParaListSize = 0;
			continue;
		}
		else if(szLine == strTmp[1])
		{
			state = 1;
			SleepParaListSize = 0;
			continue;
		}
		else if(szLine == strTmp[2])
		{
			state = 2;
			AF_InitParaListSize = 0;
			continue;
		}
		else if(szLine == strTmp[3])
		{
			state = 3;
			AF_AutoParaListSize = 0;
			continue;
		}
		else if(szLine == strTmp[4])
		{
			state = 4;
			AF_FarParaListSize = 0;
			continue;
		}
		else if(szLine == strTmp[5])
		{
			state = 5;
			AF_NearParaListSize = 0;
			continue;
		}
		else if(szLine == strTmp[6])
		{
			state = 6;
			Exposure_ParaListSize = 0;
			continue;
		}
		else if(szLine == strTmp[7])
		{
			state = 7;
			Gain_ParaListSize = 0;
			continue;
		}

		if(szLine.IsEmpty())
			continue;
		if(szLine.Left(1) == ",")
			continue;
		if(szLine.Left(1) == ";")
			continue;
		if(szLine.Left(1) == "/")
			continue;

		if(szLine.Left(1) == "[")
		{
			state = -1;
			continue;
		}


		AfxExtractSubString(sReg, szLine, 0, ',');
		AfxExtractSubString(sVal, szLine, 1, ',');
		sReg.TrimLeft();   
		sReg.TrimRight();
		sVal.TrimRight();  
		sVal.TrimLeft();

		if(!sscanf_s(sReg, "0x%x", &reg)) //读取键值对数据	
			sscanf_s(sReg, "%d", &reg);

		if(!sscanf_s(sVal, "0x%x", &value)) //读取键值对数据	
			sscanf_s(sVal, "%d", &value);

		if(state == 0)
		{
			*(pParaList+ParaListSize) = reg;
			*(pParaList+ParaListSize+1) = value;
			ParaListSize += 2;
		}
		else if(state == 1)
		{
			*(pSleepParaList+SleepParaListSize) = reg;
			*(pSleepParaList+SleepParaListSize+1) = value;
			SleepParaListSize += 2;			
		}
		else if(state == 2)
		{
			*(pAF_InitParaList+AF_InitParaListSize) = reg;
			*(pAF_InitParaList+AF_InitParaListSize+1) = value;
			AF_InitParaListSize += 2;			
		}
		else if(state == 3)
		{
			*(pAF_AutoParaList+AF_AutoParaListSize) = reg;
			*(pAF_AutoParaList+AF_AutoParaListSize+1) = value;
			AF_AutoParaListSize += 2;			
		}
		else if(state == 4)
		{
			*(pAF_FarParaList+AF_FarParaListSize) = reg;
			*(pAF_FarParaList+AF_FarParaListSize+1) = value;
			AF_FarParaListSize += 2;			
		}
		else if(state == 5)
		{
			*(pAF_NearParaList+AF_NearParaListSize) = reg;
			*(pAF_NearParaList+AF_NearParaListSize+1) = value;
			AF_NearParaListSize += 2;			
		}
		else if(state == 6)
		{
			*(pExposure_ParaList+Exposure_ParaListSize) = reg;
			*(pExposure_ParaList+Exposure_ParaListSize+1) = value;
			Exposure_ParaListSize += 2;			
		}
		else if(state == 7)
		{
			*(pGain_ParaList+Gain_ParaListSize) = reg;
			*(pGain_ParaList+Gain_ParaListSize+1) = value;
			Gain_ParaListSize += 2;			
		}

	}
	file.Close();

	if(ParaListSize)
	{
		pSensor->ParaListSize = ParaListSize ;// + 2; //datasize...
		pSensor->ParaList = m_pSensorPara;

		if(SleepParaListSize)
		{
			pSensor->SleepParaListSize = SleepParaListSize;
			pSensor->SleepParaList = m_pSensorSleepPara;
		}
		if(AF_InitParaListSize)
		{
			pSensor->AF_InitParaListSize = AF_InitParaListSize;
			pSensor->AF_InitParaList = m_pAF_InitParaList;
		}
		if(AF_AutoParaListSize)
		{
			pSensor->AF_AutoParaListSize = AF_AutoParaListSize;
			pSensor->AF_AutoParaList = m_pAF_AutoParaList;
		}
		if(AF_FarParaListSize)
		{
			pSensor->AF_FarParaListSize = AF_FarParaListSize;
			pSensor->AF_FarParaList = m_pAF_FarParaList;
		}
		if(AF_NearParaListSize)
		{
			pSensor->AF_NearParaListSize = AF_NearParaListSize;
			pSensor->AF_NearParaList = m_pAF_NearParaList;
		}
		if(Exposure_ParaListSize)
		{
			pSensor->Exposure_ParaListSize = Exposure_ParaListSize;
			pSensor->Exposure_ParaList = m_pExposure_ParaList;
		}
		if(Gain_ParaListSize)
		{
			pSensor->Gain_ParaListSize = Gain_ParaListSize;
			pSensor->Gain_ParaList = m_pGain_ParaList;
		}
		return TRUE;
	}

	return FALSE;
}
//read sensor setting from .ini file
int LoadIniFile(SensorTab *pCurrentSensor, const char *configFile)
{
	int iRet = -1;
	SensorTab NewSensor;
	memset(&NewSensor,0,sizeof(SensorTab));
	SetIniFileName(configFile);


	NewSensor.width    = ReadIniData("Sensor","width",0);
	NewSensor.height   = ReadIniData("Sensor","height",0);
	NewSensor.type     = ReadIniData("Sensor","type",2);

	NewSensor.port = ReadIniData("Sensor", "port", 0);
	NewSensor.pin = ReadIniData("Sensor", "pin", 0);

	NewSensor.SlaveID  = ReadIniData("Sensor", "SlaveID", 0);
	NewSensor.mode     = ReadIniData("Sensor", "mode", 0);
	NewSensor.FlagReg  = ReadIniData("Sensor", "FlagReg", 0);
	NewSensor.FlagMask = ReadIniData("Sensor", "FlagMask", 0xff);
	NewSensor.FlagData = ReadIniData("Sensor", "FlagData", 0);

	NewSensor.FlagReg1  = ReadIniData("Sensor", "FlagReg1", 0);
	NewSensor.FlagMask1 = ReadIniData("Sensor", "FlagMask1", 0x0);
	NewSensor.FlagData1 = ReadIniData("Sensor", "FlagData1", 0);

	NewSensor.outformat= ReadIniData("Sensor", "outformat", 0x00);
	NewSensor.mclk     = ReadIniData("Sensor", "mclk", 0x01);

	NewSensor.avdd     = ReadIniData("Sensor", "avdd", 0x00);
	NewSensor.dovdd     = ReadIniData("Sensor", "dovdd", 0x00);
	NewSensor.dvdd     = ReadIniData("Sensor", "dvdd", 0x00);

	ClearIniFileName();

	NewSensor.ParaList = NULL;
	NewSensor.ParaListSize = 0;
	NewSensor.SleepParaList = NULL;
	NewSensor.SleepParaListSize = NULL;

	bGetI2CDataFromLibFile(configFile, &NewSensor);
	if( (NewSensor.width==0)       ||
		(NewSensor.height==0)      ||
		(NewSensor.ParaList==NULL) ||
		(NewSensor.ParaListSize==0)	  )
	{
		return FALSE;
	}
	memcpy(pCurrentSensor,&NewSensor,sizeof(SensorTab));
	iRet = 1;
	return iRet;
}

int OpenCamera(int devID, const char *configFile)
{
	int iRet = DT_ERROR_OK;
	SensorTab sCurrentSensor;

	//load sensor ini
	USHORT SensorPara[8192 * 4];
	memset(SensorPara, 0, sizeof(USHORT) * 8192 * 4);
	sCurrentSensor.ParaList = SensorPara;
	iRet = LoadIniFile(&sCurrentSensor, configFile);

	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}

	//set io pin (reset/pwdn,scl, sda, mclk to low)
	SensorEnable(0, 1, devID);
	//关闭IO上拉电阻
	SetSoftPinPullUp(IO_NOPULL, devID);
	//20151116 added to close the mclk...
	SetSensorClock(FALSE,(USHORT)(m_fMclk*10), devID); 

	/*first set sensor working condition....*/
	{
		//first set pin definition...
		{
			BYTE  pinDef[40] = {0};
			//mipi....
			//if(m_PortSel.GetCurSel() == 0)
			
			{
				pinDef[0] = 20;
				pinDef[1] = 0;
				pinDef[2] = 2;
				pinDef[3] = 1;
				pinDef[4] = 3;
				pinDef[5] = 4;
				pinDef[6] = 5;
				pinDef[7] = 6;
				pinDef[8] = 7;
				pinDef[9] = 8;
				pinDef[10] = 9;
				pinDef[11] = 20;
				pinDef[12] = 10;
				pinDef[13] = 11;
				pinDef[14] = 12;
				pinDef[15] = 20;
				pinDef[16] = 20;
				pinDef[17] = 13;
				pinDef[18] = 15;
				pinDef[19] = 14;
				pinDef[20] = 19;
				pinDef[21] = 18;
				pinDef[22] = 20;
				pinDef[23] = 16;
				pinDef[24] = 20;
				pinDef[25] = 20;

			}
			
			//配置柔性接口
			SetSoftPin(pinDef,devID);
		}

		//使能柔性接口
		EnableSoftPin(TRUE,devID);
		EnableGpio(TRUE,devID);
		//set voltage and mclk.....

		////4.240 20151116 changed the power on code... to resolve the ov sensor(ov5670)
		//设置电压，电流
		SENSOR_POWER Power[10] = {POWER_AVDD, POWER_DOVDD, POWER_DVDD, POWER_AFVCC, POWER_VPP};
		int Volt[10] = {0};
		int Current[10] = {300, 300, 300, 300, 300};//300mA
		BOOL OnOff[10] = {TRUE, TRUE, TRUE, TRUE, TRUE};
		CURRENT_RANGE range[5] = {CURRENT_RANGE_MA, CURRENT_RANGE_MA, CURRENT_RANGE_MA, CURRENT_RANGE_MA, CURRENT_RANGE_MA};



		//20151116 added... close the power firstly...
		// 		//设置5路电压值0, close the power firstly, voltage set to zero....
		if (PmuSetVoltage(Power, Volt,5, devID) != DT_ERROR_OK)
		{
			CloseDevice(devID);
			AfxMessageBox("Set Voltage Failed!");
			return FALSE;
		}
		//wait for the power is all to zero....
		Sleep(50);
		//设置电压开关 switch to off
		if (PmuSetOnOff(Power, OnOff, 5, devID) != DT_ERROR_OK)
		{
			CloseDevice(devID);
			AfxMessageBox("Close Power Failed!");
			return FALSE;
		}

		if (SetSensorClock(TRUE,(USHORT)(m_fMclk*10), devID) != DT_ERROR_OK)
		{
			CloseDevice(devID);
			AfxMessageBox("Set Mclk Failed!");
			return FALSE;
		}
		Sleep(1);

#if 0
		//20151116 power on the sensor...////		//first power the avdd.
		// 1. power the avdd. 
		OnOff[POWER_AVDD] = TRUE;
		Volt[POWER_AVDD] = (int)(m_fAvdd * 1000); // 2.8V
		PmuSetOnOff(Power,OnOff,5,devID);
		PmuSetVoltage(Power, Volt,5, devID);
		Sleep(1);

		// 2, power the dovdd...
		OnOff[POWER_DOVDD] = TRUE;
		Volt[POWER_DOVDD] = (int)(m_fDovdd * 1000); // 1.8V
		PmuSetOnOff(Power,OnOff,5,devID);
		PmuSetVoltage(Power, Volt,5, devID);
		Sleep(5);

		// 3, power on the  dvdd and the afvcc...
		OnOff[POWER_DVDD] = TRUE;
		Volt[POWER_DVDD] = (int)(m_fDvdd * 1000);// 1.2V

		OnOff[POWER_AFVCC] = TRUE;
		Volt[POWER_AFVCC] = (int)(m_fAfvcc * 1000); // 2.8V
		Volt[POWER_VPP] = (int)(m_fVpp * 1000); 
		PmuSetOnOff(Power,OnOff,5,devID);
		PmuSetVoltage(Power, Volt,5, devID);
#endif
#if 1
		Volt[POWER_DOVDD] = (int)(m_fDovdd * 1000); // 1.8V
		PmuSetVoltage(Power, Volt,5, devID);
		Sleep(2);

		Volt[POWER_DVDD] = (int)(m_fDvdd * 1000);// 1.2V
		PmuSetVoltage(Power, Volt,5, devID);
		Sleep(2);

		Volt[POWER_AVDD] = (int)(m_fAvdd * 1000); // 2.8V
		PmuSetVoltage(Power, Volt,5, devID);
		Sleep(2);
		Volt[POWER_AFVCC] = (int)(m_fAfvcc * 1000);
		PmuSetVoltage(Power, Volt,5, devID);
		Sleep(2);// 2.8V
		Volt[POWER_VPP] = (int)(m_fVpp * 1000); 
		PmuSetVoltage(Power, Volt,5, devID);
		Sleep(2);
#endif
		//should wait for 50ms to be ready...
		Sleep(50);

		// 设置量程
		PmuSetCurrentRange(Power,range,5,devID);

		//设置电流
		PmuSetOcpCurrentLimit(Power,Current,5,devID);


		//开启IO上拉电阻
		SetSoftPinPullUp(IO_PULLUP, devID);
	}
	Sleep(10);
	//i2C init....

	//设置SENSOR I2C的速率为400Kbps,允许从设备为Streching mode（从设备端可以拉低scl和sda电平来表示busy）
	SetSensorI2cRate(I2C_400K, devID);
	//
	SetSensorI2cRapid(0, devID);
	SetI2CInterval(0, devID); //I2C byte to byte delay
	//check sensor is on line or not ,if on line,init sensor to work....
	{
		SensorEnable(sCurrentSensor.pin ^ 0x02, 1, devID); //reset
		Sleep(20);
		SensorEnable(sCurrentSensor.pin, 1, devID);
		Sleep(50);

		//check sensoris on line...
		if(SensorIsMe(&sCurrentSensor, CHANNEL_A, 0,devID) != DT_ERROR_OK)
		{
			AfxMessageBox("Sensor is not ok");
			return FALSE;			
		}
		//init sensor....
		if(InitSensor(sCurrentSensor.SlaveID,
			sCurrentSensor.ParaList,
			sCurrentSensor.ParaListSize,
			sCurrentSensor.mode,devID) != DT_ERROR_OK)
		{
			AfxMessageBox("Init Sensor Failed!");
			return FALSE;			
		}
	}
	m_isTV = FALSE;
	USHORT TVBoard_Flag = 0;

	ReadSensorReg(0xba, 0x80, &TVBoard_Flag, I2CMODE_MICRON, devID);
	if(TVBoard_Flag == 0x5150)
	{
		m_isTV = 1;
	}	

	USHORT pValue[10] = {0};

	if(ReadSensorReg(0x40, 0x000C, pValue, I2CMODE_MICRON2, devID) ==  DT_ERROR_OK)
	{
		CString str;
		str.Format("%s",pValue);


	}
	//set image property...
#if 0
	//for external eeprom write and read check....
	BYTE myData[8] = {0, 2, 4, 6, 8, 5, 6, 7};
	BYTE RetData[8] = {0};
	UCHAR SlaveID = 0xa2;
	int nRet = WriteSensorI2c(SlaveID, 0x00, 2, myData, 8);
	if(DT_ERROR_OK == nRet)
	{
		//wait write bytes ended....
		int i;
		for(i = 0; i < 100; i++)
		{
			if(DT_ERROR_OK == WriteSensorI2c(SlaveID, 0x00, 0, 0, 0))
			{
				break;
			}
			//Sleep(1);
		}
		// 		CString stmp;
		// 		stmp.Format("i = %d", i);
		// 		AfxMessageBox(stmp);
		if(i >= 100)
		{
			AfxMessageBox("i2c busy!");
			return FALSE;
		}
		//end wait....

		nRet = ReadSensorI2c(SlaveID, 0x00, 2, RetData, 8, 1);
		if(nRet == DT_ERROR_OK)
		{
			for(i = 0; i < 8; i++)
			{
				if(RetData[i] != myData[i])
				{
					AfxMessageBox("check error!");
					return FALSE;
				}
			}
			if(i == 8)
			{
				AfxMessageBox("check ok!");
			}
		}
		else
		{
			AfxMessageBox("read error!");
			return FALSE;
		}
	}
	else
	{
		AfxMessageBox("write error!");
		return FALSE;
	}
#endif

	//end check....
	if(sCurrentSensor.type == D_YUV || sCurrentSensor.type == D_YUV_SPI || sCurrentSensor.type == D_YUV_MTK_S)
		SetYUV422Format(sCurrentSensor.outformat, devID);
	else
		SetRawFormat(sCurrentSensor.outformat, devID);


	USHORT roi_x0 = sCurrentSensor.width >> 2;
	USHORT roi_y0 = sCurrentSensor.height >> 2;
	USHORT roi_hb = 0;
	USHORT roi_vb = 0;
	USHORT roi_hnum = 1;
	USHORT roi_vnum = 1;

	USHORT fifo_div = 2;	
	roi_x0 = 0;
	roi_y0 = 0;
	roi_hb = 0;
	roi_vb = 0;
	roi_hnum = 1;
	roi_vnum = 1;
	//初始化设备
	InitRoi(0, 0, sCurrentSensor.width, m_isTV ? sCurrentSensor.height >> 1 :sCurrentSensor.height , 0, 0, 1, 1, sCurrentSensor.type, TRUE, devID);	//以像素为单位，全分辨率显示关闭ROI使能
	SetSensorPort(sCurrentSensor.port, sCurrentSensor.width, sCurrentSensor.height, devID);


	//only useful for pe300/pe810/pe910 series....

	//调整MIPI RX CLOCK相位
	SetMipiClkPhase(0,devID);

	Sleep(10);
	CalculateGrabSize(&m_GrabSize, devID);

	//open video....
	OpenVideo(m_GrabSize,devID);

	//malloc memory and create the thread....
	{
		UINT nSize = sCurrentSensor.width * sCurrentSensor.height * 3 + 1024;

// 		m_pTripleBuffer = (LPBYTE)malloc(nSize);
// 		m_pCameraBuffer = (LPBYTE)malloc(nSize);
// 		m_pDisplayBuffer = (LPBYTE)malloc(nSize);
// 
// 		if (m_pTripleBuffer  == NULL  || 
// 			m_pCameraBuffer  == NULL  || 
// 			m_pDisplayBuffer == NULL 
// 			)
// 		{
// 			AfxMessageBox("Memory error!");
// 			return FALSE;
// 		}
// 		memset(m_pTripleBuffer, 0, nSize);
// 		memset(m_pCameraBuffer, 0, nSize);
// 		memset(m_pDisplayBuffer, 0, nSize);
	}

	//thread....

	return iRet;
}

int CloseCamera(int devID, const char *configFile)
{
	int iRet = DT_ERROR_OK;
	//for power down
	iRet = CloseVideo(devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}

	// Set reset pin, pwdn pin as a non working mode
	ResetSensorI2cBus(devID);
	int iRstPwdPin = GetPrivateProfileInt(("Sensor"), ("pin"), 0, configFile);
	BYTE Pwdn2 = 0;
	BYTE Pwdn1 = 0;
	BYTE Reset = 0;
	Pwdn2 = iRstPwdPin & PWDN_H ? PWDN2_L : PWDN2_H;   //pwdn2 neg to pwdn1
	Pwdn1 = iRstPwdPin & PWDN_H ? PWDN_H : PWDN_L;     //pwdn1
	Reset = iRstPwdPin & RESET_H ? RESET_H : RESET_L;  //reset
	iRstPwdPin = Pwdn2 | Pwdn1 | Reset;
	iRet = SensorEnable(iRstPwdPin, false, devID); //reset
	Sleep(20);

	// close mclk
	iRet = SetSensorClock(false, 24 * 10, devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}

	// close softpin
	iRet = SetSoftPinPullUp(FALSE, devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}
	iRet = EnableSoftPin(FALSE, devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}
	iRet = EnableGpio(FALSE, devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}

	//power off
	SENSOR_POWER Power[10] = { POWER_AVDD, POWER_DOVDD, POWER_DVDD, POWER_AFVCC, POWER_VPP };
	int Volt[10] = { 0 };
	BOOL OnOff[10] = { FALSE };
	iRet = PmuSetVoltage(Power, Volt, 5, devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}
	Sleep(50);
	iRet = PmuSetOnOff(Power, OnOff, 5, devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}

	return iRet;
}

//dothinkey mipi raw10 to std raw10
void MipiRaw10toRaw8(BYTE *pIn, BYTE *pOut, USHORT nWidth, USHORT nHeight)
{
	for (long i = 0; i < nWidth*nHeight * 5 / 4; i = i + 5)
	{
		*pOut++ = pIn[i];
		*pOut++ = pIn[i + 1];
		*pOut++ = pIn[i + 2];
		*pOut++ = pIn[i + 3];
	}
}

int SaveRaw8(const char *sfilename, unsigned char *pRaw, int nWidth, int nHeight)
{
	int iRet = DT_ERROR_OK;
	HANDLE hRawFILE = CreateFile(sfilename, GENERIC_WRITE | GENERIC_READ, FILE_SHARE_WRITE | FILE_SHARE_READ, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hRawFILE == INVALID_HANDLE_VALUE)
	{
		return DT_ERROR_FILE_CREATE_FAILED;
	}
	UINT imagesize = nWidth*nHeight;
	DWORD dwWritten; 
	WriteFile(hRawFILE, pRaw, imagesize, &dwWritten, NULL);
	CloseHandle(hRawFILE);
	return iRet;
}

int main()
{
    int nRetCode_12M = 0;
	//int nRetCode_20M = 0;
	m_pSensorName = new char [256];   //(char*) malloc(256*sizeof(char));
	m_pSensorPara = new USHORT [8192*4];   //(USHORT*) malloc(8192*sizeof(USHORT));
	m_pSensorSleepPara = new USHORT [2048];   //(USHORT*) malloc(1024*2);

	//20130823 added..
	m_pAF_InitParaList = new USHORT [8192];
	m_pAF_AutoParaList = new USHORT [2048];
	m_pAF_FarParaList = new USHORT [2048];
	m_pAF_NearParaList = new USHORT [2048];
	m_pExposure_ParaList = new USHORT [2048];
	m_pGain_ParaList = new USHORT [2048];


	memset(m_pSensorPara, 0, 8192*4);
	memset(m_pSensorSleepPara, 0, 2048);


	WriteSensorReg(0x18,0x00,0x01,I2CMODE_NORMAL);
	WriteSensorReg(0x18,0x00,0x00,I2CMODE_NORMAL);
	WriteSensorReg(0x18,0x01,0x01,I2CMODE_NORMAL);

	TCHAR szFilePath[MAX_PATH + 1] = { 0 };
	GetModuleFileName(NULL, szFilePath, MAX_PATH);
	(_tcsrchr(szFilePath, _T('\\')))[1] = 0; // 删除文件名，只获得路径字串
	CString sConfigPath_12M = szFilePath;
	sConfigPath_12M += "sony_4L_3016_12M.ini";

	//Enumerate Device and open Device
	int nDeviceCnt = 0;
	char *DeviceName[4] = { NULL };
	CString m_DevName[20] = {};
	int i;
	int nRetID_12M = -1;
	//int nRetID_20M = -1;
	EnumerateDevice(DeviceName, 4, &nDeviceCnt);
	if (nDeviceCnt == 0)
	{
		printf("No dothinkey device found\n");
		return 0;
	}
	else
	{
		printf("EnumerateDevice nDeviceCnt %d:\n", nDeviceCnt);
	}
	for (i = 0; i<nDeviceCnt; i++)
	{
		m_DevName[i].Empty();
		if (DeviceName[i] != NULL)
		{
			m_DevName[i].Format("%s", DeviceName[i]);
			printf("Device%d:%s\n", i, DeviceName[i]);
			if (i == 0)
			{
				nRetCode_12M = OpenDevice(m_DevName[i], &nRetID_12M, i);
				if (nRetCode_12M != 1)
				{
					printf("%s:OpenDevice fail error code=%d\n", DeviceName[i], nRetCode_12M);
				}
			}
			/*if (i == 1)
			{
				nRetCode_20M = OpenDevice(m_DevName[i], &nRetID_20M, i);
				if (nRetCode_20M != 1)
				{
					printf("%s:OpenDevice fail error code=%d\n", DeviceName[i], nRetCode_20M);
				}
			}*/
			GlobalFree(DeviceName[i]);
		}
	}

	//Open Camera
	nRetCode_12M = OpenCamera(nRetID_12M, sConfigPath_12M);
	if (nRetCode_12M != DT_ERROR_OK)
	{
		printf("OpenCamera fail error code=%d\n", nRetCode_12M);
		return nRetCode_12M;
	}
	//if(m_RunMode != RUNMODE_STOP)
	{
		unsigned char ucSndDat = 0;
		int cnt = 0;

		ucSndDat = SelectDownload(0,6);
		SetGyroOffset(0,0);
		SetAngleCorrection(0,6);
		RemapMain();
		WitTim(100);

		do{
			if(cnt++ > 10){
				ucSndDat = 0xFF;
				break;
			}
		}while(RdStatus(0) == 0x01);
	}
	//int nLoop_12M = 0;
	//CString sTemp_12M = "";
	unsigned int iWidth_12M = GetPrivateProfileInt(_T("Sensor"), _T("width"), 0, sConfigPath_12M);
	unsigned int iHeight_12M = GetPrivateProfileInt(_T("Sensor"), _T("height"), 0, sConfigPath_12M);
	/*"C:\\work\\zhanglei\\项目\\ConsoleDemo\\Debug\\IMX214_4L_3120_063_34.ini"*/
	
	//picture object with various format
	unsigned char* pRawBuf_12M = new unsigned char[iWidth_12M * iHeight_12M * 3 + 1024];
	unsigned char* pRaw8Buf_12M = new unsigned char[iWidth_12M * iHeight_12M];

	FrameInfo m_FrameInfo;

	// change 1: brightness
	int write_0k_12M = WriteSensorReg(0x34, 0x0202, 0x30, 3, nRetID_12M);//brightness
	if (write_0k_12M != DT_ERROR_OK)
	{
		printf("brightness Reg write erorr\n");
	}
	Sleep(300);

	//CString sConfigPath = szFilePath;
	//sConfigPath += "sony_4L_3016_12M.ini";          // get the config file's address

	int nStart, nEnd;
	int nStep = 5;

	// change 2: start and end number
	nStart = 650;
	nEnd = 700;

	//nStart += (nStep * 1);
	int cir = 0;
	int number = 0;
	while (nStart <= nEnd/* && number++ < 3*/)
	{
		USHORT uValue = nStart;
		BYTE   dataBuf[10];
		{
			dataBuf[0] = (BYTE)(uValue >> 24);
			dataBuf[1] = (BYTE)((uValue >> 16) & 0x00FF);
			dataBuf[2] = (BYTE)((uValue & 0xFFFF) >> 8);
			dataBuf[3] = (BYTE)(uValue & 0x00FF);

			//dataBuf[0] = (BYTE)(uValue & 0x00FF);
			//dataBuf[1] = (BYTE)((uValue & 0xFFFF) >> 8);
			//dataBuf[2] = (BYTE)((uValue >> 16) & 0x00FF);
			//dataBuf[3] = (BYTE)(uValue >> 24);
		}
		//cout << "dataBuf[0] = " << (USHORT)dataBuf[0] << endl;
		//cout << "dataBuf[1] = " << (USHORT)dataBuf[1] << endl;
		//cout << "dataBuf[2] = " << (USHORT)dataBuf[2] << endl;
		//cout << "dataBuf[3] = " << (USHORT)dataBuf[3] << endl;
		//int n2Ret = WriteSensorReg(0x7C, 0xF01A, 0x0384, 4, nRetID_12M);
		int n2Ret = WriteSensorI2c(0x7C, 0xF01A, 2, dataBuf, 4);
		if (n2Ret == 1)
		{
			//printf("VCM write %d success\n", nStart);
		}
		else
		{
			printf("VCM write %d fail\n", nStart);
		}
		if (cir < 1)
		{
			cir++;
			Sleep(200);
		}

		ULONG RetSize = 0;
		//int nRetCode = 0;
		//int nLoop = 0;
		//CString sTemp = "";
		//unsigned int iWidth = GetPrivateProfileInt(_T("Sensor"), _T("width"), 0, sConfigPath_12M);
		//unsigned int iHeight = GetPrivateProfileInt(_T("Sensor"), _T("height"), 0, sConfigPath_12M/*"C:\\work\\zhanglei\\项目\\ConsoleDemo\\Debug\\IMX214_4L_3120_063_34.ini"*/);
		//unsigned char *pRawBuf = new unsigned char[iWidth * iHeight * 3 + 1024];
		//unsigned char *pRaw8Buf = new unsigned char[iWidth * iHeight];

		nRetCode_12M = GrabFrame(pRawBuf_12M, m_GrabSize, &RetSize, &m_FrameInfo, nRetID_12M);
		Sleep(200);
		if (nRetCode_12M != DT_ERROR_OK)
		{
			printf("Grab Frame fail error code=%d\n", nRetCode_12M);
			continue;
		}
		MipiRaw10toRaw8(pRawBuf_12M, pRaw8Buf_12M, iWidth_12M, iHeight_12M);
		/*char sFileName[40];
		if (nStart < 1000)
		{
			sprintf_s(sFileName, "src/12M_0500mm_VCM0%d.raw", nStart);
		}
		else
		{
			sprintf_s(sFileName, "src/12M_0500mm_VCM%d.raw", nStart);
		}*/
		//sTemp.Format(sFileName, nLoop++);
		if (cir >= 1)
		{
			//SaveRaw8(sTemp, pRaw8Buf, iWidth, iHeight);//raw8 8bit
			//printf("save image %s\n", sFileName);

			Mat iris_img = Mat(iHeight_12M, iWidth_12M, CV_8UC1, pRaw8Buf_12M);
			cvtColor(iris_img, iris_img, COLOR_BayerRG2RGB);
			
			//size of matrix
			int height = iris_img.rows;
			int width = iris_img.cols;

			//5-Area ROI center
			int center_ROI_A[2]; 
			int center_ROI_B[2];
			int center_ROI_C[2];
			int center_ROI_D[2];
			int center_ROI_E[2];

			//upper left
			center_ROI_A[0] = int(height / 4);
			center_ROI_A[1] = int(height / 4);

			//upper right
			center_ROI_B[0] = int(height / 4);
			center_ROI_B[1] = int(3 * height / 4);

			//lower left
			center_ROI_C[0] = int(3 * height / 4);
			center_ROI_C[1] = int(height / 4);

			//lower right
			center_ROI_D[0] = int(3 * height / 4);
			center_ROI_D[1] = int(3 * height / 4);

			//center
			center_ROI_E[0] = int(height / 2);
			center_ROI_E[1] = int(height / 2);

			//5-Area ROI size
			int height_ROI = int(height / 18);
			int width_ROI = int(width / 18);

			//half size
			int half_height_ROI = int(height / 36);
			int half_width_ROI = int(width / 36);

			//amount of pixel in ROI
			int area_ROI = height_ROI * width_ROI;

			//ROI matrix
			int* ROI_A = new int[area_ROI];
			int* ROI_B = new int[area_ROI];
			int* ROI_C = new int[area_ROI];
			int* ROI_D = new int[area_ROI];
			int* ROI_E = new int[area_ROI];

			//construct img gray//
			Mat img_gray(height, width, CV_8UC1);
			cvtColor(iris_img, img_gray, CV_BGR2GRAY);

			//give value to ROI matrix object

			//A
			int i_start = center_ROI_A[0] - half_height_ROI;
			int j_start = center_ROI_A[1] - half_width_ROI;

			for (int i = 0; i < height_ROI; i++) {

				for (int j = 0; j < width_ROI; j++) {

					ROI_A[i * width_ROI + j] = img_gray.ptr<uchar>(i_start + i)[j_start + j];

				}
			}
			
			//sizeof(ROI_A) stands for size of index variable
			//cout << sizeof(ROI_A) << endl;

			//_msize(ROI_A）represent the array size to which the index points
			//cout << _msize(ROI_A) << endl;

			cout << bool(_msize(ROI_A) / sizeof(ROI_A[0]) == area_ROI) << endl;

			//vector<int> compression_params;
			//compression_params.push_back(COLOR_IMWRITE_PNG_STRATEGY_DEFAULT);
			//compression_params.push_back(100);
			//imwrite("D:/tmp/new.png", iris_img, compression_params);
			//namedWindow("iris_img", CV_WINDOW_NORMAL);
			//pyrDown(iris_img, iris_img, Size(iris_img.cols / 2, iris_img.rows / 2));//
			//resizeWindow("iris_img", 1200, 900);
			//imshow("iris_img", iris_img);
			//resize(iris_img, iris_img, Size(3968, 2976), 0, 0, INTER_LINEAR);//
			char name[50];//the problem "buffer too small" once raised
			printf("");
			printf("-->VCM Code: %d\n", nStart);
			// change 3: save path
			if (nStart < 1000)
			{
				
				sprintf_s(name, "C:/Users/Administrator/Desktop/Test/tmp0%d.jpg", nStart);
			}
			else
			{
				sprintf_s(name, "C:/Users/Administrator/Desktop/Test/tmp%d.jpg", nStart);
			}

			
			//imwrite(name, iris_img);//
			//waitKey(0);
			//destroyWindow("iris_img");
			iris_img.release();
		}
		nStart += nStep;
	}

	delete[] pRaw8Buf_12M;
	system("PAUSE");
	CloseCamera(nRetID_12M, sConfigPath_12M);
	CloseDevice(nRetID_12M);
    return nRetCode_12M;
}