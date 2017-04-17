package com.tourist.root.touristnyc;

import android.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;

/**
 * Created by USER on 4/11/2017.
 */

public class Tab1 extends android.support.v4.app.Fragment {

    protected static int[] layoutIDs = {R.id.infoLayout, R.id.interestLayout};

    protected void viewUserDetails(View view)  {

        Button button = (Button) view.findViewById(R.id.detailsButton);
        if (button != null) {
            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    clearLayouts(v);
                    LinearLayout infoLayout = (LinearLayout) v.findViewById(R.id.infoLayout);
                    infoLayout.setVisibility(View.VISIBLE);
                }
            });
        }
    }

    protected void viewPOIs(View view)  {

        Button button = (Button) view.findViewById(R.id.interestButton);
        if (button != null) {
            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {

                    clearLayouts(v);
                    LinearLayout interestLayout = (LinearLayout) v.findViewById(R.id.interestLayout);
                    interestLayout.setVisibility(View.VISIBLE);
                }
            });
        }
    }

    protected void clearLayouts(View view)   {

        for (int i=0; i<layoutIDs.length; i++)      {

            LinearLayout layout = (LinearLayout) view.findViewById(layoutIDs[i]);
            layout.setVisibility(View.GONE);
        }
    }


    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, Bundle savedInstanceState) {
        View v =  inflater.inflate(R.layout.tab1, container, false);
        viewPOIs(v);
        viewUserDetails(v);
        return v;
    }
}
