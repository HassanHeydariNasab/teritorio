package com.hsn6.teritorio;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.net.Uri;
import android.content.Intent;
import android.view.View;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.widget.Toast;
import android.content.Context;
import android.app.AlertDialog;
import android.content.DialogInterface;
import com.hsn6.teritorio.util.*;
import java.io.IOException;
import android.webkit.JavascriptInterface;
import java.util.Arrays;
import android.content.pm.PackageManager;
import android.content.pm.PackageInfo;
import android.webkit.WebChromeClient;
import android.webkit.JsResult;

public class main_activity extends Activity
{
    WebView myWebView;
    IabHelper mHelper;
    static String sku = "";
    static final String sku100 = "blokoj100";
    static final String sku200 = "blokoj200";
    static final String sku500 = "blokoj500";
    static final String sku1000 = "blokoj1000";
    String nl = "";
    private static final String TAG = "MyActivity";
    String base64EncodedPublicKey = "MIHNMA0GCSqGSIb3DQEBAQUAA4G7ADCBtwKBrwDv4SowX/nV9nyqQRLaxtvXtdUpludohGUsi88gkNBVC9V3a/aLZlRom0H4gYEsECARubBGbE24y3gXaA/y/C1WrHgnCQB1u8+QtuyYAPzz8AQbk0iKiMz6v9y28IkbILj/gVNLkoNNyf7UlKWmpAd7jE2SV9m89cpFj0LDT6LFzX8bYeBw8n1M3bgQc5C0/HFlCV/gFhbHhBAQM6S9p5qkx57EBMCHyAz0egOpJ6UCAwEAAQ==";
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
	
	mHelper = new IabHelper(this, base64EncodedPublicKey);
	mHelper.enableDebugLogging(true);

	this.myWebView = (WebView) findViewById(R.id.webview);
	myWebView.addJavascriptInterface(main_activity.this, "Android");
	WebSettings webSettings = myWebView.getSettings();
	webSettings.setJavaScriptEnabled(true);
	webSettings.setDomStorageEnabled(true);
	webSettings.setAllowFileAccess(true);
	webSettings.setAllowContentAccess(true);
	webSettings.setAllowUniversalAccessFromFileURLs(true);
	//webSettings.setAllowFileAccessFromFileURLs(true);
	myWebView.setWebViewClient(new WebViewClient());
	myWebView.setWebChromeClient(new WebChromeClient() {
        public void onProgressChanged(WebView view, int progress) {
            main_activity.this.setProgress(progress * 1000);
        };
		@Override
		public boolean onJsAlert(WebView view, String url, String message, final android.webkit.JsResult result)
		{
		    new AlertDialog.Builder(main_activity.this)
			.setTitle(R.string.alert)
			.setMessage(message)
			.setPositiveButton(R.string.ok,
					   new AlertDialog.OnClickListener()
					   {
					       public void onClick(DialogInterface dialog, int wicht)
					       {
						   result.confirm();
					       }
					   }).setCancelable(false)
			.create()
			.show();
		    return true;
		};
		@Override
		public boolean onJsConfirm(WebView view, String url, String message, final JsResult result) {
		    new AlertDialog.Builder(main_activity.this)
			.setTitle(R.string.confirm)
			.setMessage(message)
			.setPositiveButton(R.string.ok,
					   new DialogInterface.OnClickListener() {
					       public void onClick(DialogInterface dialog, int which) {
						   result.confirm();
					       }
					   }).setNegativeButton(R.string.cancel, 
								new DialogInterface.OnClickListener() {
								    public void onClick(DialogInterface dialog, int which) {
									result.cancel();
								    }
								}).setCancelable(false).create().show();
		    return true;
		};
	    });	
	myWebView.setOnLongClickListener(new View.OnLongClickListener() {
		@Override
	    public boolean onLongClick(View v) {
		return true;
	    }
	});
	myWebView.setLongClickable(false);
	// disable scroll on touch
	myWebView.setOnTouchListener(new View.OnTouchListener() {
		@Override
		public boolean onTouch(View v, MotionEvent event) {
		    return (event.getAction() == MotionEvent.ACTION_MOVE);
		}
	    });
	//myWebView.setVerticalScrollBarEnabled(false);
	myWebView.setHorizontalScrollBarEnabled(false);
	if(isPackageExisted("com.farsitel.bazaar")){
	    mHelper.startSetup(new IabHelper.OnIabSetupFinishedListener() {
		    public void onIabSetupFinished(IabResult result) {
			Log.d(TAG, "Setup finished.");
			
			if (!result.isSuccess()) {
			    // Oh noes, there was a problem.
			    Log.d(TAG,"Problem setting up in-app billing: " + result);
			    return;
			}
			
			// Have we been disposed of in the meantime? If so, quit.
			if (mHelper == null) return;
			
			// IAB is fully set up. Now, let's get an inventory of stuff we own.
			Log.d(TAG, "Setup successful. Querying inventory.");
			mHelper.queryInventoryAsync(mGotInventoryListener);
		    }
		});
	}
	myWebView.loadUrl("file:///android_asset/ludo.html");
    }
    public boolean isPackageExisted(String targetPackage){
	PackageManager pm=getPackageManager();
	try {
	    PackageInfo info=pm.getPackageInfo(targetPackage,PackageManager.GET_META_DATA);
	} catch (PackageManager.NameNotFoundException e) {
	    return false;
	}  
	return true;
    }
    // Listener that's called when we finish querying the items and subscriptions we own
    IabHelper.QueryInventoryFinishedListener mGotInventoryListener = new IabHelper.QueryInventoryFinishedListener() {
	    public void onQueryInventoryFinished(IabResult result, Inventory inventory) {
		Log.d(TAG, "Query inventory finished.");
		
		// Have we been disposed of in the meantime? If so, quit.
		if (mHelper == null) return;
		
		// Is it a failure?
		if (result.isFailure()) {
		    Log.d(TAG, "Failed to query inventory: " + result);
		    return;
		}
		
		Log.d(TAG, "Query inventory was successful.");
		
		/*
		 * Check for items we own. Notice that for each purchase, we check
		 * the developer payload to see if it's correct! See
		 * verifyDeveloperPayload().
		 */
		
		// Check for gas delivery -- if we own gas, we should fill up the tank immediately
		Purchase gasPurchase = inventory.getPurchase(sku100);
		if (gasPurchase != null && verifyDeveloperPayload(gasPurchase)) {
		    Log.d(TAG, "We have sku100. Consuming it.");
		    mHelper.consumeAsync(inventory.getPurchase(sku100), mConsumeFinishedListener);
		    return;
		}
		gasPurchase = inventory.getPurchase(sku200);
		if (gasPurchase != null && verifyDeveloperPayload(gasPurchase)) {
		    Log.d(TAG, "We have sku200. Consuming it.");
		    mHelper.consumeAsync(inventory.getPurchase(sku200), mConsumeFinishedListener);
		    return;
		}
		gasPurchase = inventory.getPurchase(sku500);
		if (gasPurchase != null && verifyDeveloperPayload(gasPurchase)) {
		    Log.d(TAG, "We have sku500. Consuming it.");
		    mHelper.consumeAsync(inventory.getPurchase(sku500), mConsumeFinishedListener);
		    return;
		}
		gasPurchase = inventory.getPurchase(sku1000);
		if (gasPurchase != null && verifyDeveloperPayload(gasPurchase)) {
		    Log.d(TAG, "We have sku1000. Consuming it.");
		    mHelper.consumeAsync(inventory.getPurchase(sku1000), mConsumeFinishedListener);
		    return;
		}
	    }
	};
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
	super.onActivityResult(requestCode, resultCode, data);
	
	Log.d(TAG, "onActivityResult(" + requestCode + "," + resultCode + "," + data);
	
	// Pass on the activity result to the helper for handling
	if (!mHelper.handleActivityResult(requestCode, resultCode, data)) {
	    super.onActivityResult(requestCode, resultCode, data);
	} else {
	    Log.d(TAG, "onActivityResult handled by IABUtil.");
	}
    }
    boolean verifyDeveloperPayload(Purchase p) {
        String payload = p.getDeveloperPayload();
        return true;
    };
    // Callback for when a purchase is finished
    IabHelper.OnIabPurchaseFinishedListener mPurchaseFinishedListener = new IabHelper.OnIabPurchaseFinishedListener() {
	    public void onIabPurchaseFinished(IabResult result, Purchase purchase)
	    {
		if (result.isFailure()) {
		    Log.d(TAG, "Error purchasing: " + result);
		    return;
		}
		if (!verifyDeveloperPayload(purchase)) {
		    Log.d(TAG, "Error purchasing. Authenticity verification failed.");
		    return;
		}

		Log.d(TAG, "Purchase successful.");

		if (purchase != null && verifyDeveloperPayload(purchase) && purchase.getPurchaseState() == 0) {
		    Log.d(TAG, "We have sku. Consuming it.");
		    mHelper.consumeAsync(purchase, mConsumeFinishedListener);
		    return;
		}
		
		/*else if (purchase.getSku().equals(sku100)) {
		  myWebView.loadUrl("javascript:window.localStorage.sku = 0;");
		  myWebView.reload();
		  }*/
	    }
	};
    // Called when consumption is complete
    IabHelper.OnConsumeFinishedListener mConsumeFinishedListener = new IabHelper.OnConsumeFinishedListener() {
        public void onConsumeFinished(Purchase purchase, IabResult result) {
            Log.d(TAG, "Consumption finished. Purchase: " + purchase + ", result: " + result);

            // if we were disposed of in the meantime, quit.
            if (mHelper == null) return;

            // We know this is the "gas" sku because it's the only one we consume,
            // so we don't check which sku was consumed. If you have more than one
            // sku, you probably should check...
            if (result.isSuccess()) {
                // successfully consumed, so we apply the effects of the item in our
                // game world's logic, which in our case means filling the gas tank a bit
                Log.d(TAG, "Consumption successful. Provisioning.");
		myWebView.loadUrl("javascript:window.localStorage.ordoj += '" + purchase.getToken() + '-' + purchase.getSku() + ",';sendi_ordojn()");
            }
            else {
                Log.d(TAG, "Error while consuming: " + result);
            }
            Log.d(TAG, "End consumption flow.");
        }
    };
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
	if (keyCode == KeyEvent.KEYCODE_BACK) {
	    new AlertDialog.Builder(this)
		//.setIcon(android.R.drawable.ic_dialog_alert)
		.setTitle(R.string.quit)
		.setMessage(R.string.really_quit)
		.setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {
			@Override
			public void onClick(DialogInterface dialog, int which) {
			    main_activity.this.finish();
			}
		    })
		.setNegativeButton(R.string.no, null)
		.show();
	    return true;
	}
	return super.onKeyDown(keyCode, event);
    }
    @JavascriptInterface
    public void acxeti_dialogo(String amount){
	if (amount.equals(sku100)){
	    sku = sku100;
	}
	else if (amount.equals(sku200)){
	    sku = sku200;
	}
	else if (amount.equals(sku500)){
	    sku = sku500;
	}
	else if (amount.equals(sku1000)){
	    sku = sku1000;
	}
	new AlertDialog.Builder(this)
	    //.setIcon(android.R.drawable.ic_dialog_alert)
	    .setTitle(R.string.buy)
	    .setMessage(R.string.really_buy)
	    .setPositiveButton(R.string.yes, new DialogInterface.OnClickListener() {
		    @Override
		    public void onClick(DialogInterface dialog, int which) {
			if(isPackageExisted("com.farsitel.bazaar")){			
			    mHelper.launchPurchaseFlow(main_activity.this, sku, 2000, mPurchaseFinishedListener, nl);
			}
			else{
			    Toast.makeText(main_activity.this, R.string.bazar_neinstalita, Toast.LENGTH_SHORT).show();
			}
		    }
		})
	    .setNegativeButton(R.string.no, null)
	    .show();
    };
    @JavascriptInterface
    public void showToast(String toast) {
        Toast.makeText(main_activity.this, toast, Toast.LENGTH_SHORT).show();
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
	
        // very important:
        Log.d(TAG, "Destroying helper.");
        if (mHelper != null) {
            mHelper.dispose();
            mHelper = null;
        }
    }
    
}
