package com.tensorflow.chatinterface;

import android.app.Application;
import android.content.Context;

import com.iflytek.cloud.SpeechConstant;
import com.iflytek.cloud.SpeechUtility;

/**
 * Date:2018-06-03
 * Time:13:03
 * Description:自定义的Application
 */
public class ChatApplication extends Application {

    //一个全局的Context变量
    public static Context sContext;
//    public static final String URL = "http://10.0.2.2:8000/api/chatbot";
    public static final String URL = "http://172.20.10.13:8000/api/chatbot";

//    public static final String URL = "http://144.214.94.231:8000/api/chatbot";
    @Override
    public void onCreate() {
        super.onCreate();
        sContext = getApplicationContext();
        initXfVoice();
    }

    //这里还有一句代码的，你这里不知道为什么没有了，我需要添加进来，等一下，我拷贝一下。。。
    private void initXfVoice() {
        // 将“12345678”替换成您申请的APPID，申请地址：http://www.xfyun.cn
        // 请勿在“=”与appid之间添加任何空字符或者转义符
        SpeechUtility.createUtility(getApplicationContext(), SpeechConstant.APPID + "=59414fec");
    }
}
