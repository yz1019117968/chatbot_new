package com.tensorflow.chatinterface.util;

import android.text.TextUtils;
import android.util.Log;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;


public class HttpUtils {
    private static final String TAG = "HttpUtils";
    public static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");
    private static OkHttpClient mClient = null;
    private static HttpUtils sInstance = null;

    private HttpUtils() {
    }

    public static HttpUtils getInstance() {
        if (null == sInstance) {
            synchronized (HttpUtils.class) {
                if (null == sInstance) {
                    sInstance = new HttpUtils();
                }
            }
        }
        return sInstance;
    }

    /**
     * 通用同步请求
     *
     * @param request
     * @return
     * @throws IOException
     */
    private Response execute(Request request) {
        mClient = new OkHttpClient.Builder()
                .connectTimeout(1, TimeUnit.MINUTES)
                .writeTimeout(5, TimeUnit.MINUTES)
                .readTimeout(5, TimeUnit.MINUTES)
                .build();
        try {
            return mClient.newCall(request).execute();
        } catch (IOException e) {
//            e.printStackTrace();
            System.out.println("exception:"+e.getMessage());
        }
        return null;

    }

    /**
     * get方式URL拼接
     *
     * @param url
     * @param message
     * @return
     */
    public String getRequestUrl(String url, String message) {
        if (TextUtils.isEmpty(message)) {
            return url;
        }
        StringBuilder newUrl = new StringBuilder(url);
        newUrl.append("?");
        newUrl.append("infos");
        newUrl.append("=");
        newUrl.append(message);
        return newUrl.toString();
    }

    /**
     * get请求获取response
     * @param url
     * @return
     */
    public String getRequest(String url) {
        System.out.println("url1:"+url);
        String responseString = null;
        Request request = new Request.Builder()
                .url(url)
                .build();
        try {
            Response response = execute(request);
            System.out.println("Response:"+response);
//            System.out.println("response.log"+response);
            responseString = response.body().string();
        } catch (IOException e) {
            e.printStackTrace();
        }
        Log.d(TAG,"responseString = " + responseString);
        return responseString;
    }
}
