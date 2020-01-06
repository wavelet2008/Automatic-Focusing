// ConsoleDemo.cpp : Defining entry points for console applications。
//

#include "stdafx.h"
#include "ConsoleDemo.h"
#include <vector>
#include "..\\DTCCM2_SDK\\dtccm2.h"
#include "IniFileRW.h"
#include "..\\LC898124EP1/DownloadCmd.h"
#include "..\\LC898124EP1/HighLevelCmd.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


// The only application object

CWinApp theApp;

using namespace std;

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
	UINT addr = 0, reg = 0, value = 0;
	BYTE i2cmode = 0;
	USHORT *pParaList = m_pSensorPara;
	USHORT *pSleepParaList = m_pSensorSleepPara;
	USHORT *pAF_InitParaList = m_pAF_InitParaList;
	USHORT *pAF_AutoParaList = m_pAF_AutoParaList;
	USHORT *pAF_FarParaList = m_pAF_FarParaList;
	USHORT *pAF_NearParaList = m_pAF_NearParaList;
	USHORT *pExposure_ParaList = m_pExposure_ParaList;
	USHORT *pGain_ParaList = m_pGain_ParaList;

	USHORT ParaListSize = 0;
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

	for (int i = 0; i < 10; i++)
	{
		strTmp[i].MakeLower();
		strTmp[i].Trim();
	}
	int state = -1;
	while (file.ReadString(szLine))
	{
		CString Textout;
		//寻找注释符号或者']',如果有这样的，只取前面的，
		tmp = szLine.FindOneOf("//");
		if (tmp == 0)
		{
			continue;
		}
		else if (tmp > 0)
		{
			szLine = szLine.Left(tmp);
		}
		tmp = szLine.FindOneOf("]");
		if (tmp == 0)
		{
			continue;
		}
		else if (tmp > 0)
		{
			szLine = szLine.Left(tmp + 1);
		}
		szLine.MakeLower();
		szLine.TrimLeft();
		szLine.TrimRight();

		if (szLine == strTmp[0])
		{
			state = 0;
			ParaListSize = 0;
			continue;
		}
		else if (szLine == strTmp[1])
		{
			state = 1;
			SleepParaListSize = 0;
			continue;
		}
		else if (szLine == strTmp[2])
		{
			state = 2;
			AF_InitParaListSize = 0;
			continue;
		}
		else if (szLine == strTmp[3])
		{
			state = 3;
			AF_AutoParaListSize = 0;
			continue;
		}
		else if (szLine == strTmp[4])
		{
			state = 4;
			AF_FarParaListSize = 0;
			continue;
		}
		else if (szLine == strTmp[5])
		{
			state = 5;
			AF_NearParaListSize = 0;
			continue;
		}
		else if (szLine == strTmp[6])
		{
			state = 6;
			Exposure_ParaListSize = 0;
			continue;
		}
		else if (szLine == strTmp[7])
		{
			state = 7;
			Gain_ParaListSize = 0;
			continue;
		}

		if (szLine.IsEmpty())
			continue;
		if (szLine.Left(1) == ",")
			continue;
		if (szLine.Left(1) == ";")
			continue;
		if (szLine.Left(1) == "/")
			continue;

		if (szLine.Left(1) == "[")
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

		if (!sscanf_s(sReg, "0x%x", &reg)) //读取键值对数据	
			sscanf_s(sReg, "%d", &reg);

		if (!sscanf_s(sVal, "0x%x", &value)) //读取键值对数据	
			sscanf_s(sVal, "%d", &value);

		if (state == 0)
		{
			*(pParaList + ParaListSize) = reg;
			*(pParaList + ParaListSize + 1) = value;
			ParaListSize += 2;
		}
		else if (state == 1)
		{
			*(pSleepParaList + SleepParaListSize) = reg;
			*(pSleepParaList + SleepParaListSize + 1) = value;
			SleepParaListSize += 2;
		}
		else if (state == 2)
		{
			*(pAF_InitParaList + AF_InitParaListSize) = reg;
			*(pAF_InitParaList + AF_InitParaListSize + 1) = value;
			AF_InitParaListSize += 2;
		}
		else if (state == 3)
		{
			*(pAF_AutoParaList + AF_AutoParaListSize) = reg;
			*(pAF_AutoParaList + AF_AutoParaListSize + 1) = value;
			AF_AutoParaListSize += 2;
		}
		else if (state == 4)
		{
			*(pAF_FarParaList + AF_FarParaListSize) = reg;
			*(pAF_FarParaList + AF_FarParaListSize + 1) = value;
			AF_FarParaListSize += 2;
		}
		else if (state == 5)
		{
			*(pAF_NearParaList + AF_NearParaListSize) = reg;
			*(pAF_NearParaList + AF_NearParaListSize + 1) = value;
			AF_NearParaListSize += 2;
		}
		else if (state == 6)
		{
			*(pExposure_ParaList + Exposure_ParaListSize) = reg;
			*(pExposure_ParaList + Exposure_ParaListSize + 1) = value;
			Exposure_ParaListSize += 2;
		}
		else if (state == 7)
		{
			*(pGain_ParaList + Gain_ParaListSize) = reg;
			*(pGain_ParaList + Gain_ParaListSize + 1) = value;
			Gain_ParaListSize += 2;
		}

	}
	file.Close();

	if (ParaListSize)
	{
		pSensor->ParaListSize = ParaListSize;// + 2; //datasize...
		pSensor->ParaList = m_pSensorPara;

		if (SleepParaListSize)
		{
			pSensor->SleepParaListSize = SleepParaListSize;
			pSensor->SleepParaList = m_pSensorSleepPara;
		}
		if (AF_InitParaListSize)
		{
			pSensor->AF_InitParaListSize = AF_InitParaListSize;
			pSensor->AF_InitParaList = m_pAF_InitParaList;
		}
		if (AF_AutoParaListSize)
		{
			pSensor->AF_AutoParaListSize = AF_AutoParaListSize;
			pSensor->AF_AutoParaList = m_pAF_AutoParaList;
		}
		if (AF_FarParaListSize)
		{
			pSensor->AF_FarParaListSize = AF_FarParaListSize;
			pSensor->AF_FarParaList = m_pAF_FarParaList;
		}
		if (AF_NearParaListSize)
		{
			pSensor->AF_NearParaListSize = AF_NearParaListSize;
			pSensor->AF_NearParaList = m_pAF_NearParaList;
		}
		if (Exposure_ParaListSize)
		{
			pSensor->Exposure_ParaListSize = Exposure_ParaListSize;
			pSensor->Exposure_ParaList = m_pExposure_ParaList;
		}
		if (Gain_ParaListSize)
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
	memset(&NewSensor, 0, sizeof(SensorTab));
	SetIniFileName(configFile);


	NewSensor.width = ReadIniData("Sensor", "width", 0);
	NewSensor.height = ReadIniData("Sensor", "height", 0);
	NewSensor.type = ReadIniData("Sensor", "type", 2);

	NewSensor.port = ReadIniData("Sensor", "port", 0);
	NewSensor.pin = ReadIniData("Sensor", "pin", 0);

	NewSensor.SlaveID = ReadIniData("Sensor", "SlaveID", 0);
	NewSensor.mode = ReadIniData("Sensor", "mode", 0);
	NewSensor.FlagReg = ReadIniData("Sensor", "FlagReg", 0);
	NewSensor.FlagMask = ReadIniData("Sensor", "FlagMask", 0xff);
	NewSensor.FlagData = ReadIniData("Sensor", "FlagData", 0);

	NewSensor.FlagReg1 = ReadIniData("Sensor", "FlagReg1", 0);
	NewSensor.FlagMask1 = ReadIniData("Sensor", "FlagMask1", 0x0);
	NewSensor.FlagData1 = ReadIniData("Sensor", "FlagData1", 0);

	NewSensor.outformat = ReadIniData("Sensor", "outformat", 0x00);
	NewSensor.mclk = ReadIniData("Sensor", "mclk", 0x01);

	NewSensor.avdd = ReadIniData("Sensor", "avdd", 0x00);
	NewSensor.dovdd = ReadIniData("Sensor", "dovdd", 0x00);
	NewSensor.dvdd = ReadIniData("Sensor", "dvdd", 0x00);

	ClearIniFileName();

	NewSensor.ParaList = NULL;
	NewSensor.ParaListSize = 0;
	NewSensor.SleepParaList = NULL;
	NewSensor.SleepParaListSize = NULL;

	bGetI2CDataFromLibFile(configFile, &NewSensor);
	if ((NewSensor.width == 0) ||
		(NewSensor.height == 0) ||
		(NewSensor.ParaList == NULL) ||
		(NewSensor.ParaListSize == 0))
	{
		return FALSE;
	}
	memcpy(pCurrentSensor, &NewSensor, sizeof(SensorTab));
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
	SetSensorClock(FALSE, (USHORT)(m_fMclk * 10), devID);

	/*first set sensor working condition....*/
	{
		//first set pin definition...
		{
			BYTE  pinDef[40] = { 0 };
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
			SetSoftPin(pinDef, devID);
		}

		//使能柔性接口
		EnableSoftPin(TRUE, devID);
		EnableGpio(TRUE, devID);
		//set voltage and mclk.....

		////4.240 20151116 changed the power on code... to resolve the ov sensor(ov5670)
		//设置电压，电流
		SENSOR_POWER Power[10] = { POWER_AVDD, POWER_DOVDD, POWER_DVDD, POWER_AFVCC, POWER_VPP };
		int Volt[10] = { 0 };
		int Current[10] = { 300, 300, 300, 300, 300 };//300mA
		BOOL OnOff[10] = { TRUE, TRUE, TRUE, TRUE, TRUE };
		CURRENT_RANGE range[5] = { CURRENT_RANGE_MA, CURRENT_RANGE_MA, CURRENT_RANGE_MA, CURRENT_RANGE_MA, CURRENT_RANGE_MA };



		//20151116 added... close the power firstly...
		// 		//设置5路电压值0, close the power firstly, voltage set to zero....
		if (PmuSetVoltage(Power, Volt, 5, devID) != DT_ERROR_OK)
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

		if (SetSensorClock(TRUE, (USHORT)(m_fMclk * 10), devID) != DT_ERROR_OK)
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
		PmuSetOnOff(Power, OnOff, 5, devID);
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(1);

		// 2, power the dovdd...
		OnOff[POWER_DOVDD] = TRUE;
		Volt[POWER_DOVDD] = (int)(m_fDovdd * 1000); // 1.8V
		PmuSetOnOff(Power, OnOff, 5, devID);
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(5);

		// 3, power on the  dvdd and the afvcc...
		OnOff[POWER_DVDD] = TRUE;
		Volt[POWER_DVDD] = (int)(m_fDvdd * 1000);// 1.2V

		OnOff[POWER_AFVCC] = TRUE;
		Volt[POWER_AFVCC] = (int)(m_fAfvcc * 1000); // 2.8V
		Volt[POWER_VPP] = (int)(m_fVpp * 1000);
		PmuSetOnOff(Power, OnOff, 5, devID);
		PmuSetVoltage(Power, Volt, 5, devID);
#endif
#if 1
		Volt[POWER_DOVDD] = (int)(m_fDovdd * 1000); // 1.8V
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);

		Volt[POWER_DVDD] = (int)(m_fDvdd * 1000);// 1.2V
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);

		Volt[POWER_AVDD] = (int)(m_fAvdd * 1000); // 2.8V
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);
		Volt[POWER_AFVCC] = (int)(m_fAfvcc * 1000);
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);// 2.8V
		Volt[POWER_VPP] = (int)(m_fVpp * 1000);
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);
#endif
		//should wait for 50ms to be ready...
		Sleep(50);

		// 设置量程
		PmuSetCurrentRange(Power, range, 5, devID);

		//设置电流
		PmuSetOcpCurrentLimit(Power, Current, 5, devID);


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
		if (SensorIsMe(&sCurrentSensor, CHANNEL_A, 0, devID) != DT_ERROR_OK)
		{
			AfxMessageBox("Sensor is not ok");
			return FALSE;
		}
		//init sensor....
		if (InitSensor(sCurrentSensor.SlaveID,
			sCurrentSensor.ParaList,
			sCurrentSensor.ParaListSize,
			sCurrentSensor.mode, devID) != DT_ERROR_OK)
		{
			AfxMessageBox("Init Sensor Failed!");
			return FALSE;
		}
	}
	m_isTV = FALSE;
	USHORT TVBoard_Flag = 0;

	ReadSensorReg(0xba, 0x80, &TVBoard_Flag, I2CMODE_MICRON, devID);
	if (TVBoard_Flag == 0x5150)
	{
		m_isTV = 1;
	}

	USHORT pValue[10] = { 0 };

	if (ReadSensorReg(0x40, 0x000C, pValue, I2CMODE_MICRON2, devID) == DT_ERROR_OK)
	{
		CString str;
		str.Format("%s", pValue);


	}
	//set image property...
#if 0
	//for external eeprom write and read check....
	BYTE myData[8] = { 0, 2, 4, 6, 8, 5, 6, 7 };
	BYTE RetData[8] = { 0 };
	UCHAR SlaveID = 0xa2;
	int nRet = WriteSensorI2c(SlaveID, 0x00, 2, myData, 8);
	if (DT_ERROR_OK == nRet)
	{
		//wait write bytes ended....
		int i;
		for (i = 0; i < 100; i++)
		{
			if (DT_ERROR_OK == WriteSensorI2c(SlaveID, 0x00, 0, 0, 0))
			{
				break;
			}
			//Sleep(1);
		}
		// 		CString stmp;
		// 		stmp.Format("i = %d", i);
		// 		AfxMessageBox(stmp);
		if (i >= 100)
		{
			AfxMessageBox("i2c busy!");
			return FALSE;
		}
		//end wait....

		nRet = ReadSensorI2c(SlaveID, 0x00, 2, RetData, 8, 1);
		if (nRet == DT_ERROR_OK)
		{
			for (i = 0; i < 8; i++)
			{
				if (RetData[i] != myData[i])
				{
					AfxMessageBox("check error!");
					return FALSE;
				}
			}
			if (i == 8)
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
	if (sCurrentSensor.type == D_YUV || sCurrentSensor.type == D_YUV_SPI || sCurrentSensor.type == D_YUV_MTK_S)
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
	InitRoi(0, 0, sCurrentSensor.width, m_isTV ? sCurrentSensor.height >> 1 : sCurrentSensor.height, 0, 0, 1, 1, sCurrentSensor.type, TRUE, devID);	//以像素为单位，全分辨率显示关闭ROI使能
	SetSensorPort(sCurrentSensor.port, sCurrentSensor.width, sCurrentSensor.height, devID);


	//only useful for pe300/pe810/pe910 series....

	//调整MIPI RX CLOCK相位
	SetMipiClkPhase(0, devID);

	Sleep(10);
	CalculateGrabSize(&m_GrabSize, devID);

	//open video....
	OpenVideo(m_GrabSize, devID);

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
	UINT imagesize = nWidth * nHeight;
	DWORD dwWritten;
	WriteFile(hRawFILE, pRaw, imagesize, &dwWritten, NULL);
	CloseHandle(hRawFILE);
	return iRet;
}

int DtEnumerateDevice(char *DeviceName[], int iDeviceNumMax, int *pDeviceNum)
{
	int iRet = DT_ERROR_OK;
	iRet = EnumerateDevice(DeviceName, iDeviceNumMax, pDeviceNum);
	return iRet;
}

int DtOpenDevice(const char *devName, int *retID, int devID)
{
	int iRet = DT_ERROR_OK;
	iRet = OpenDevice(devName, retID, devID);
	return iRet;
}

int LoadIniFile(pSensorTab2 pCurrentSensor, const char *configFile)
{
	int iRet = -1;
	pCurrentSensor->width = GetPrivateProfileInt(_T("Sensor"), _T("width"), 0, configFile);
	pCurrentSensor->height = GetPrivateProfileInt(_T("Sensor"), _T("height"), 0, configFile);
	pCurrentSensor->type = GetPrivateProfileInt(_T("Sensor"), _T("type"), 2, configFile);
	pCurrentSensor->port = GetPrivateProfileInt(_T("Sensor"), _T("port"), 0, configFile);
	pCurrentSensor->pin = GetPrivateProfileInt(_T("Sensor"), _T("pin"), 0, configFile);
	pCurrentSensor->SlaveID = GetPrivateProfileInt(_T("Sensor"), _T("SlaveID"), 0, configFile);
	pCurrentSensor->mode = GetPrivateProfileInt(_T("Sensor"), _T("mode"), 0, configFile);
	pCurrentSensor->outformat = GetPrivateProfileInt(_T("Sensor"), _T("outformat"), 0, configFile);
	//i2c\mclk\voltage
	pCurrentSensor->iicrate = GetPrivateProfileInt(_T("Sensor"), _T("iicrate"), 400, configFile);
	pCurrentSensor->mclk = GetPrivateProfileInt(_T("Sensor"), _T("mclk"), 24, configFile);
	pCurrentSensor->avdd = GetPrivateProfileInt(_T("Sensor"), _T("avdd"), 2800, configFile);
	pCurrentSensor->dovdd = GetPrivateProfileInt(_T("Sensor"), _T("dovdd"), 1800, configFile);
	pCurrentSensor->dvdd = GetPrivateProfileInt(_T("Sensor"), _T("dvdd"), 1200, configFile);
	pCurrentSensor->afvcc = GetPrivateProfileInt(_T("Sensor"), _T("afvcc"), 2800, configFile);
	pCurrentSensor->vpp = GetPrivateProfileInt(_T("Sensor"), _T("vpp"), 0, configFile);

	char retStringBuf[37002];
	int iRetSize = 0;
	iRetSize = GetPrivateProfileSectionA("ParaList", retStringBuf, 37002, configFile);//The maximum profile section size is 32,767 characters.
	if (37000 == iRetSize)
	{
		return 0;//超出最大字节数
	}

	vector<string>::size_type i = 0;
	int j = 0;
	int k = 0;
	int iSensorData;
	string sTemp;
	while (j < iRetSize)
	{
		if (retStringBuf[j] == 0 || j == 0)
		{
			if (j == 0)
				sTemp = &retStringBuf[j];
			else
				sTemp = &retStringBuf[j + 1];

			if (sTemp != "")
			{
				if (sTemp[0] != '/' && sTemp[0] != ';')
				{
					vector<string> vecSensorData = split(sTemp, (" ,*/"));
					for (i = 0; i != vecSensorData.size(); ++i)
					{
						if (sscanf_s(vecSensorData[i].data(), "0x%x", &iSensorData) == 1)
						{
							//sscanf_s(vecSensorData[i].data(),("%d"), &iSensorData);
							pCurrentSensor->ParaList[k] = iSensorData;
							k++;
						}

					}
				}
			}

		}
		j++;

	}
	pCurrentSensor->ParaListSize = k;
	iRet = 1;
	return iRet;
}

int DtOpenCamera(int devID, const char *configFile)
{
	int iRet = DT_ERROR_OK;
	SensorTab2 sCurrentSensor;

	////加载sensor ini
	unsigned int SensorPara[8192 * 4];
	memset(SensorPara, 0, sizeof(unsigned int) * 8192 * 4);
	sCurrentSensor.ParaList = SensorPara;
	iRet = LoadIniFile(&sCurrentSensor, configFile);

	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}

	// 初始化柔性IO
	{
		unsigned char PinDef[26] = { PIN_NC };
		PinDef[0] = PIN_CLK_ADJ_18M;
		PinDef[1] = 0;//PIN_D0
		PinDef[2] = 2;//PIN_D2
		PinDef[3] = 1;//PIN_D1
		PinDef[4] = 3;//PIN_D3
		PinDef[5] = 4;//PIN_D4
		PinDef[6] = 5;//PIN_D5
		PinDef[7] = 6;//PIN_D6
		PinDef[8] = 7;//PIN_D7
		PinDef[9] = 8;//PIN_D8
		PinDef[10] = 9;//PIN_D9
		PinDef[11] = 20;//PIN_NC
		PinDef[12] = 10;//PIN_PCLK
		PinDef[13] = 11;//PIN_HSYNC
		PinDef[14] = 12;//PIN_VSYNC
		PinDef[15] = 20;//PIN_NC
		PinDef[16] = 20;//PIN_NC
		PinDef[17] = 13;//PIN_MCLK
		PinDef[18] = 15;//PIN_PWDN
		PinDef[19] = 14;//PIN_RESET
		PinDef[20] = 19;//PIN_SCL
		PinDef[21] = 18;//PIN_SDA
		PinDef[22] = PIN_NC;//PIN_GPIO2;//PinDef[22]对应测试盒上的PO2
		PinDef[23] = PIN_NC;//PIN_GPIO1;//PinDef[23]对应测试盒上的PO1
		PinDef[24] = PIN_NC;//PIN_GPIO3;//PinDef[24]对应测试盒上的PO3
		PinDef[25] = PIN_NC;//PIN_GPIO4;//PinDef[25]对应测试盒上的PO4

		iRet = SetSoftPin(PinDef, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}

		iRet = EnableSoftPin(TRUE, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}

		iRet = SetSoftPinPullUp(TRUE, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}

		iRet = EnableGpio(TRUE, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}
	}

	//Open Power/IO/Mclk
	{
		SENSOR_POWER Power[10] = { POWER_AVDD, POWER_DOVDD, POWER_DVDD, POWER_AFVCC, POWER_VPP };
		int Volt[10] = { 0 };
		int Current[10] = { 600, 600, 600, 600, 100 };
		int Rise[10] = { 100, 100, 100, 100, 100 };
		int SampleSpeed[5] = { 200,200,200,200,200 };
		BOOL OnOff[10] = { TRUE, TRUE, TRUE, TRUE, TRUE };
		CURRENT_RANGE range[5] = { CURRENT_RANGE_MA, CURRENT_RANGE_MA, CURRENT_RANGE_MA, CURRENT_RANGE_MA, CURRENT_RANGE_MA };

		// 设置电压斜率
		iRet = PmuSetRise(Power, Rise, 5, devID);

		iRet = PmuSetSampleSpeed(Power, SampleSpeed, 5, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}

		//set all power  to 0, close the power firstly, voltage set to zero....
		if (PmuSetVoltage(Power, Volt, 5, devID) != DT_ERROR_OK)
		{
			CloseDevice(devID);
			return FALSE;
		}
		//wait for the power is all to zero....
		Sleep(50);
		//set PmuSetOnOff is On...
		iRet = PmuSetOnOff(Power, OnOff, 5, devID);
		if (iRet != DT_ERROR_OK)
		{
			CloseDevice(devID);
			return iRet;
		}
		//wait for the PmuSetOnOff is On....
		Sleep(50);
		// 1, power the dovdd...
		Volt[POWER_DOVDD] = (int)(sCurrentSensor.dovdd); // 1.8V
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);

		// 2. power the avdd. 
		Volt[POWER_AVDD] = (int)(sCurrentSensor.avdd); // 2.8V
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);

		// 3, power on the  dvdd 
		Volt[POWER_DVDD] = (int)(sCurrentSensor.dvdd);// 1.2V
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);

		//4. power the afvcc ...
		Volt[POWER_AFVCC] = (int)(sCurrentSensor.afvcc); // 2.8V
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);
		//5. power the vpp...
		Volt[POWER_VPP] = (int)(sCurrentSensor.vpp);
		PmuSetVoltage(Power, Volt, 5, devID);
		Sleep(2);

		//设置限流
		iRet = PmuSetOcpCurrentLimit(Power, Current, 5, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}
		// 设置量程
		iRet = PmuSetCurrentRange(Power, range, 5, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}

		//设置时钟输入 switch to on...
		iRet = SetSensorClock(TRUE, (USHORT)(sCurrentSensor.mclk * 10), devID);
		if (iRet != DT_ERROR_OK)
		{
			CloseDevice(devID);
			return DT_ERROR_FAILED;
		}
		Sleep(50);
	}

	//i2C init....
	SetSensorI2cRateEx(sCurrentSensor.iicrate, devID);//设置iic速率
	SetSensorI2cRapid(0, devID);//设置推挽模式
	SetI2CInterval(0, devID);//I2C byte to byte delay
	SetSensorI2cAckWait(100, devID);//ACK等待
	SetMipiImageVC(0, TRUE, 1, devID);//设置VC通道

	{
		// 设置reset pin, pwdn pin
		BYTE Pwdn2 = 0;
		BYTE Pwdn1 = 0;
		BYTE Reset = 0;

		SensorEnable(sCurrentSensor.pin^RESET_H, TRUE, devID);
		Sleep(50);
		SensorEnable(sCurrentSensor.pin, TRUE, devID);
		Sleep(50);

		Pwdn2 = sCurrentSensor.pin & PWDN_H ? PWDN2_L : PWDN2_H;   //pwdn2 neg to pwdn1
		Pwdn1 = sCurrentSensor.pin & PWDN_H ? PWDN_H : PWDN_L;     //pwdn1
		Reset = sCurrentSensor.pin & RESET_H ? RESET_H : RESET_L;  //reset

		sCurrentSensor.pin = Pwdn2 | Pwdn1 | Reset;
		iRet = SensorEnable(sCurrentSensor.pin, 1, devID); //reset

		//check sensor is on line...
		/*if(SensorIsMe(&sCurrentSensor, CHANNEL_A, 0,devID) != DT_ERROR_OK)
		{
		return FALSE;
		}*/
		//init sensor....

		iRet = InitSensor2(sCurrentSensor.SlaveID, sCurrentSensor.ParaList, sCurrentSensor.ParaListSize, sCurrentSensor.mode, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}
	}

	//初始化设备
	iRet = InitDevice(NULL, sCurrentSensor.width, sCurrentSensor.height, sCurrentSensor.port, sCurrentSensor.type, CHANNEL_A, NULL, devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}
	//end check....
	if (sCurrentSensor.type == D_YUV || sCurrentSensor.type == D_YUV_SPI || sCurrentSensor.type == D_YUV_MTK_S)
	{
		iRet = SetYUV422Format(sCurrentSensor.outformat, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}
	}
	else
	{
		iRet = SetRawFormat(sCurrentSensor.outformat, devID);
		if (iRet != DT_ERROR_OK)
		{
			return iRet;
		}
	}

	iRet = SetRoiEx(0, 0, sCurrentSensor.width, sCurrentSensor.height, 3, 3, 1, 1, 1, devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}
	//only useful for pe300/pe810/pe910 series....
	//调整MIPI RX CLOCK相位
	SetMipiClkPhase(0, devID);
	SetMipiEnable(TRUE, devID);//LP or HS 
	Sleep(10);

	iRet = OpenVideo(sCurrentSensor.width*sCurrentSensor.height * 4, devID);//为了支持精准采集P10、RGB24，图像大小要设置的大些
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}

	return iRet;
}

int DtCaptureImage(int devID, unsigned char **pImage, FrameInfoEx *pInfo)
{
	int iRet = DT_ERROR_OK;
	iRet = GrabFrameDirect(pImage, pInfo, devID);
	return iRet;
}

int DtCloseCamera(int devID, const char *configFile)
{
	int iRet = DT_ERROR_OK;
	//for power down
	iRet = CloseVideo(devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}
	ResetSensorI2cBus(devID);
	int iRstPwdPin = GetPrivateProfileInt(("Sensor"), ("pin"), 0, configFile);
	SensorEnable(iRstPwdPin ^ 3, 1, devID);
	Sleep(50);
	iRet = SetSensorClock(0, 24 * 10, devID);
	if (iRet != DT_ERROR_OK)
	{
		return iRet;
	}
	SENSOR_POWER Power[10] = { POWER_AVDD, POWER_DOVDD, POWER_DVDD, POWER_AFVCC, POWER_VPP };
	int Volt[10] = { 0 };
	BOOL OnOff[10] = { FALSE };
	SensorEnable(iRstPwdPin, FALSE, devID);
	//关闭电源
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

	// 关闭柔性接口
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

	return iRet;
}

int DtCloseDevice(int devID)
{
	int iRet = -1;
	iRet = CloseDevice(devID);
	return iRet;
}

//int Raw2Photo()
//{
//
//}

int Printing()
{
	clock_t start, finish;
	double totaltime;
	start = clock();

	int nRetCode = 0;
	m_pSensorName = new char[256];   //(char*) malloc(256*sizeof(char));
	m_pSensorPara = new USHORT[8192 * 4];   //(USHORT*) malloc(8192*sizeof(USHORT));
	m_pSensorSleepPara = new USHORT[2048];   //(USHORT*) malloc(1024*2);

	//20130823 added..
	m_pAF_InitParaList = new USHORT[8192];
	m_pAF_AutoParaList = new USHORT[2048];
	m_pAF_FarParaList = new USHORT[2048];
	m_pAF_NearParaList = new USHORT[2048];
	m_pExposure_ParaList = new USHORT[2048];
	m_pGain_ParaList = new USHORT[2048];

	memset(m_pSensorPara, 0, 8192 * 4);
	memset(m_pSensorSleepPara, 0, 2048);

	WriteSensorReg(0x18, 0x00, 0x01, I2CMODE_NORMAL);
	WriteSensorReg(0x18, 0x00, 0x00, I2CMODE_NORMAL);
	WriteSensorReg(0x18, 0x01, 0x01, I2CMODE_NORMAL);

	/*
	HMODULE hModule = ::GetModuleHandle(nullptr);

	if (hModule != nullptr)
	{
		// 初始化 MFC 并在失败时显示错误
		if (!AfxWinInit(hModule, nullptr, ::GetCommandLine(), 0))
		{
			// TODO: 更改错误代码以符合您的需要
			wprintf(L"error: MFC initialization failed\n");
			nRetCode = 1;
		}
		else
		{
			// TODO: 在此处为应用程序的行为编写代码。
		}
	}
	else
	{
		// TODO: 更改错误代码以符合您的需要
		wprintf(L"error: GetModuleHandle failed\n");
		nRetCode = 1;
	}
	*/

	TCHAR szFilePath[MAX_PATH + 1] = { 0 };
	GetModuleFileName(NULL, szFilePath, MAX_PATH);
	(_tcsrchr(szFilePath, _T('\\')))[1] = 0; // 删除文件名，只获得路径字串
	CString sConfigPath = szFilePath;
	//puts(sConfigPath);
	sConfigPath += "sony_4L_3016_12M.ini";

	//Enumerate Device and open Device
	int nDeviceCnt = 0;
	char *DeviceName[4] = { NULL };
	CString m_DevName[20] = {};
	int i;
	int nRetID = -1;
	EnumerateDevice(DeviceName, 4, &nDeviceCnt);
	if (nDeviceCnt == 0)
	{
		printf("No dothinkey device found\n");
		return 0;
	}
	for (i = 0; i < nDeviceCnt; i++)
	{
		m_DevName[i].Empty();
		if (DeviceName[i] != NULL)
		{
			m_DevName[i].Format("%s", DeviceName[i]);
			printf("Device%d:%s\n", i, DeviceName[i]);
			nRetCode = OpenDevice(m_DevName[i], &nRetID, i);
			if (nRetCode != 1)
			{
				printf("%s:OpenDevice fail error code=%d\n", DeviceName[i], nRetCode);
			}
			GlobalFree(DeviceName[i]);
		}
	}

	//Open Camera
	nRetID = 0;
	nRetCode = OpenCamera(nRetID, sConfigPath);
	if (nRetCode != DT_ERROR_OK)
	{
		printf("OpenCamera fail error code=%d\n", nRetCode);
		return nRetCode;
	}
	//if(m_RunMode != RUNMODE_STOP)
	{
		unsigned char ucSndDat = 0;
		int cnt = 0;

		ucSndDat = SelectDownload(0, 6);
		SetGyroOffset(0, 0);
		SetAngleCorrection(0, 6);
		RemapMain();
		WitTim(100);

		do {
			if (cnt++ > 10) {
				ucSndDat = 0xFF;
				break;
			}
		} while (RdStatus(0) == 0x01);
	}
	int nLoop = 0;
	CString sTemp = "";
	unsigned int iWidth = GetPrivateProfileInt(_T("Sensor"), _T("width"), 0, sConfigPath);
	unsigned int iHeight = GetPrivateProfileInt(_T("Sensor"), _T("height"), 0, sConfigPath/*"C:\\work\\zhanglei\\项目\\ConsoleDemo\\Debug\\IMX214_4L_3120_063_34.ini"*/);
	unsigned char *pRawBuf = new unsigned char[iWidth*iHeight * 3 + 1024];
	unsigned char *pRaw8Buf = new unsigned char[iWidth*iHeight];
	FrameInfo m_FrameInfo;

	/*
	// read current VCM code
	USHORT pValue = 0;
	int n1Ret = ReadSensorReg(0x7C, 0xF01A, &pValue, 4, nRetID);
	if (n1Ret == DT_ERROR_OK)
	{
		printf("VCM read sucess\n");
		printf("VCM value %d \n", pValue);
	}
	else
	{
		printf("VCM read fail\n");
	}
	*/

	// read current VCM code, default position: hex: 0x0400 dec: 1024
	unsigned char readValue[4] = { 0 };
	int nRet = ReadSensorI2c(I2C_SLAVE_ADDRESS7, 0xF01A, 2, readValue, 4);
	printf("vcm value (readValue[3210]) %d%d%d%d \n", readValue[3], readValue[2], readValue[1], readValue[0]);
	//Sleep(1000);
	//printf("Cai: ConsoleDemo: value of readValue[1] %d \n", readValue[1]);
	//printf("Cai: ConsoleDemo: value of readValue[2] %d \n", readValue[2]);
	//printf("Cai: ConsoleDemo: value of readValue[3] %d \n", readValue[3]);

	int nMdlNum = 11;
	//printf("请输入模组号：");
	//scanf_s("%d", &nMdlNum);

	int nStart;
	int nEnd;
	int nStep = 4;
	switch (nMdlNum) {
		case 1:
			nStart = 888;
			nEnd = 1276;
			break;
		case 2:
			nStart = 920;
			nEnd = 1284;
			break;
		case 3:
			nStart = 882;
			nEnd = 1270;
			break;
		case 4:
			nStart = 910;
			nEnd = 1294;
			break;
		case 5:
			nStart = 908;
			nEnd = 1292;
			break;
		case 6:
			nStart = 886;
			nEnd = 1290;
			break;
		case 7:
			nStart = 890;
			nEnd = 1274;
			break;
		case 8:
			nStart = 888;
			nEnd = 1284;
			break;
		case 9:
			nStart = 886;
			nEnd = 1282;
			break;
		case 10:
			nStart = 874;
			nEnd = 1290;
			break;
		case 11:
			nStart = 892;
			nEnd = 1308;
			break;
		default:
			puts("没有该模组");
			exit(1);
	}
	puts("下面开始彩色打印：");
	nStart -= (nStep * 1);
	int cir = 0;
	while (nStart <= nEnd)
	{
		USHORT uValue = nStart;
		BYTE	dataBuf[10];
		{
			dataBuf[0] = (BYTE)(uValue >> 24);
			dataBuf[1] = (BYTE)((uValue >> 16) & 0x00FF);
			dataBuf[2] = (BYTE)((uValue & 0xFFFF) >> 8);
			dataBuf[3] = (BYTE)(uValue & 0x00FF);
		}
		//cout << "dataBuf[0] = " << dataBuf[0] << endl;
		//cout << "dataBuf[1] = " << dataBuf[1] << endl;
		//cout << "dataBuf[2] = " << dataBuf[2] << endl;
		//cout << "dataBuf[3] = " << dataBuf[3] << endl;
		//int n2Ret = WriteSensorReg(0x7C, 0xF01A, 0x0384, 4, nRetID);
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
			Sleep(200);
		}

		ULONG RetSize = 0;
		nRetCode = GrabFrame(pRawBuf, m_GrabSize, &RetSize, &m_FrameInfo, nRetID);
		if (nRetCode != DT_ERROR_OK)
		{
			printf("Grab Frame fail error code=%d\n", nRetCode);
			continue;
		}
		MipiRaw10toRaw8(pRawBuf, pRaw8Buf, iWidth, iHeight);
		char sFileName[40];
		if (nStart < 1000)
		{
			sprintf_s(sFileName, "src/12M_0500mm_VCM0%d.raw", nStart);
		}
		else
		{
			sprintf_s(sFileName, "src/12M_0500mm_VCM%d.raw", nStart);
		}
		sTemp.Format(sFileName, nLoop++);
		if (cir >= 1)
		{
			SaveRaw8(sTemp, pRaw8Buf, iWidth, iHeight);//raw8 8bit
			printf("save image %s\n", sFileName);
		}
		cir++;
		nStart += nStep;
	}
	//delete[] pRaw8Buf;
	//system("PAUSE");
	//CloseCamera(nRetID, sConfigPath);
	//CloseDevice(nRetID);
	//return nRetCode;
	puts("");


	nRetCode = 0;
	HMODULE hModule = ::GetModuleHandle(nullptr);
	if (hModule != nullptr)
	{
		// 初始化 MFC 并在失败时显示错误
		if (!AfxWinInit(hModule, nullptr, ::GetCommandLine(), 0))
		{
			// TODO: 更改错误代码以符合您的需要
			wprintf(L"错误: MFC 初始化失败\n");
			nRetCode = 1;
		}
		else
		{
			// TODO: 在此处为应用程序的行为编写代码。
		}
	}
	else
	{
		// TODO: 更改错误代码以符合您的需要
		wprintf(L"错误: GetModuleHandle 失败\n");
		nRetCode = 1;
	}
	sConfigPath = "D:\\Kamerawerk\\Hardware\\ConsoleDemo\\ConsoleDemo\\Debug\\IMX350_4L_3840_063_34.ini";
	//枚举测试盒，打开测试盒
	nDeviceCnt = 0;
	memset(DeviceName, '0', sizeof(DeviceName));
	//char *DeviceName[12] = { NULL };
	memset(m_DevName, '0', sizeof(m_DevName));
	//CString m_DevName[20] = {};
	nRetID = -1;
	DtEnumerateDevice(DeviceName, 12, &nDeviceCnt);
	//上电、供时钟、初始化摄像头、点亮
	nRetID = 1;
	nRetCode = DtOpenCamera(nRetID, sConfigPath);
	//printf("code = %d, id = %d\n", nRetCode, nRetID);
	if (nRetCode != DT_ERROR_OK)
	{
		printf("DtOpenCamera fail error code=%d\n", nRetCode);
		return nRetCode;
	}
	else
	{
		printf("Open camera %s succeeded\n", sConfigPath);
	}

	nLoop = 0;
	sTemp = "";
	iWidth = GetPrivateProfileInt(_T("Sensor"), _T("width"), 0, sConfigPath);
	iHeight = GetPrivateProfileInt(_T("Sensor"), _T("height"), 0, sConfigPath/*"C:\\work\\zhanglei\\项目\\ConsoleDemo\\Debug\\IMX214_4L_3120_063_34.ini"*/);
	pRawBuf = NULL;
	pRaw8Buf = new unsigned char[iWidth*iHeight];
	FrameInfoEx m_FrameInfo1;

	// brightness
	int write_0k = WriteSensorReg(0x34, 0x0202, 0x02, 3, nRetID);//brightness
	if (write_0k != DT_ERROR_OK)
	{
		printf("brightness write erorr\n");
	}
	//Sleep(300);

	USHORT pValue = 0;
	int uRg = 3;

	//初始化driver ic
	int write_ini_ok = WriteSensorReg(0x18, 0x02, 0x01, 0, nRetID);//PD mode enable
	if (write_ini_ok != DT_ERROR_OK)
	{
		printf("driver ic ini erorr\n");
	}
	Sleep(3);
	WriteSensorReg(0x18, 0x02, 0x00, 0, nRetID);//PD mode disable(normal operating)
	Sleep(3);
	WriteSensorReg(0x18, 0x02, 0x02, 0, nRetID);//Ringing Mode setting
	Sleep(3);
	WriteSensorReg(0x18, 0x06, 0x40, 0, nRetID);//SAC mode 3 setting, DIV2=0
	Sleep(3);
	WriteSensorReg(0x18, 0x07, 0x60, 0, nRetID);//DIV[1:0]=b'01, SACT[5:0] = b'100101
	Sleep(3);

	nStep = 3;
	switch (nMdlNum) {
		case 1:
			nStart = 393;
			nEnd = 615;
			break;
		case 2:
			nStart = 395;
			nEnd = 617;
			break;
		case 3:
			nStart = 399;
			nEnd = 621;
			break;
		case 4:
			nStart = 397;
			nEnd = 619;
			break;
		case 5:
			nStart = 405;
			nEnd = 627;
			break;
		case 6:
			nStart = 397;
			nEnd = 619;
			break;
		case 7:
			nStart = 405;
			nEnd = 627;
			break;
		case 8:
			nStart = 404;
			nEnd = 626;
			break;
		case 9:
			nStart = 369;
			nEnd = 639;
			break;
		case 10:
			nStart = 390;
			nEnd = 630;
			break;
		case 11:
			nStart = 385;
			nEnd = 625;
			break;
		default:
			puts("没有该模组");
			exit(1);
	}
	puts("下面开始黑白打印：");
	nStart -= (nStep * 1);
	cir = 0;
	while (nStart <= nEnd)
	{
		// write VCM
		int write_vcm_ok = WriteSensorReg(0x18, 0x03, nStart, 2, nRetID); //write VCM
		if (write_vcm_ok != DT_ERROR_OK)
		{
			printf("VCM pos=%d write erorr\n", nStart);
		}
		//Sleep(5);

		// acquire and save raw image
		nRetCode = DtCaptureImage(nRetID, &pRawBuf, &m_FrameInfo1);//采集到度信raw10数据
		if (nRetCode != DT_ERROR_OK)
		{
			printf("CaptureImage fail error code=%d\n", nRetCode);
			continue;
		}
		MipiRaw10toRaw8(pRawBuf, pRaw8Buf, iWidth, iHeight);
		char sFileName[40];
		sprintf_s(sFileName, "src/20M_0500mm_VCM0%d.raw", nStart);
		sTemp.Format(sFileName, nLoop++);
		if (cir++ >= 1)
		{
			SaveRaw8(sTemp, pRaw8Buf, iWidth, iHeight);
			printf("save image %s\n", sFileName);
		}
		nStart += nStep;
	}
	delete[] pRaw8Buf;

	finish = clock();
	totaltime = (double)(finish - start) / CLOCKS_PER_SEC;
	cout << "\n此程序的运行时间为" << totaltime << "秒！" << endl;

	system("PAUSE");
	DtCloseCamera(nRetID, sConfigPath);
	DtCloseDevice(nRetID);
	return nRetCode;
}

int main()
{
	Printing();
	return 0;
}