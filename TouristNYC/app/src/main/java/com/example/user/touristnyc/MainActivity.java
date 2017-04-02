package com.example.user.touristnyc;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;

public class MainActivity extends AppCompatActivity {

    protected static int[] layoutIDs = {R.id.infoLayout, R.id.interestLayout, R.id.groupLayout};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        viewUserDetails();
        viewPOIs();
        viewGroups();
    }

    protected void viewUserDetails()  {

        Button button = (Button) findViewById(R.id.detailsButton);
        if (button != null) {
            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    clearLayouts();
                    LinearLayout infoLayout = (LinearLayout) findViewById(R.id.infoLayout);
                    infoLayout.setVisibility(View.VISIBLE);
                }
            });
        }
    }

    protected void viewPOIs()  {

        Button button = (Button) findViewById(R.id.interestButton);
        if (button != null) {
            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    clearLayouts();
                    LinearLayout interestLayout = (LinearLayout) findViewById(R.id.interestLayout);
                    interestLayout.setVisibility(View.VISIBLE);
                }
            });
        }
    }

    protected void viewGroups()  {

        Button button = (Button) findViewById(R.id.groupsButton);
        if (button != null) {
            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    clearLayouts();
                    LinearLayout groupLayout = (LinearLayout) findViewById(R.id.groupLayout);
                    groupLayout.setVisibility(View.VISIBLE);
                }
            });
        }
    }

    protected void clearLayouts()   {

        for (int i=0; i<layoutIDs.length; i++)      {

            LinearLayout layout = (LinearLayout) findViewById(layoutIDs[i]);
            layout.setVisibility(View.GONE);
        }
    }
}
