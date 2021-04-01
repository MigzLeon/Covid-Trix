package com.example.firebaseheartratemonitor;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.os.Bundle;
import android.widget.Button;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {


     RecyclerView mRecyclerView;
     RecyclerView recyclerView;
     DatabaseReference reff;

     FirebaseDatabase db = FirebaseDatabase.getInstance();
     DatabaseReference mbase = db.getReference().child("Covitrix");
     ArrayList<Sensor> list;
     Button moveTempDataBtn;
    private TextView task_text,spo2,time,temp,bpm;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        reff = db.getInstance().getReference().child("sensors").child("1");
        setContentView(R.layout.activity_sensor_list);
        spo2 =(TextView) findViewById(R.id.SPO2);
        time =(TextView) findViewById(R.id.time);
        temp =(TextView) findViewById(R.id.temp);
        bpm =(TextView) findViewById(R.id.BPM);


//        mRecyclerView = (RecyclerView) findViewById(R.id.recyclerview_sensors);
//        mRecyclerView.setLayoutManager(new LinearLayoutManager(this));
//        mRecyclerView.smoothScrollBy(0,1);
//        list = new ArrayList<>();
        System.out.println("**********////////////***********");
//        System.out.println(reff.child("Member").child("1").toString());
        System.out.println("sdsdsdsdddsds222@@@@@@@@@@@@@@@@");
        String name =reff.child("SPO2").toString();
        System.out.println(name);
//        String namex =reff.;
//        reff.addValueEventListener(new ValueEventListener() {
//
//        })
//        System.out.println(namex);
//
//
//        new FirebaseHelper().readSensors(new FirebaseHelper.DataStatus() {
//            @Override
//            public void DataIsLoaded(List<Sensor> sensor, List<String> keys) {
//                new RecyclerView_Config().setConfig(mRecyclerView,MainActivity.this, sensor , keys);
//
//
//            }
//
//            @Override
//            public void DataIsInserted() {
//
//            }
//
//            @Override
//            public void DataIsUpdated() {
//
//            }
//
//            @Override
//            public void DataIsDeleted() {
//
//            }
//        });



//
        recyclerView = findViewById(R.id.recyclerview_sensors);
//
        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.smoothScrollBy(0,1);
        list = new ArrayList<>();
//
        moveTempDataBtn = findViewById(R.id.moveTempDataBtn);

        // Connecting object of required Adapter class to
        // the Adapter class itself
//        adapter = new MyAdapter(this, list);
        // Connecting Adapter class with the Recycler view*/
//        recyclerView.setAdapter(adapter);

        reff.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
//                String name = snapshot.child("age").getValue().toString();
                System.out.println("sdsdsdsdddsds222@@@@@@@@@@@@@@@@");

                System.out.println(snapshot.child("Temperature").getValue().toString());
                System.out.println(snapshot.child("TimeDate").getValue().toString());
                System.out.println(snapshot.child("HeartRate").getValue().toString());
                System.out.println(snapshot.child("SPO2").getValue().toString());
                time.setText(snapshot.child("TimeDate").getValue().toString());
                temp.setText(snapshot.child("Temperature").getValue().toString());
                bpm.setText(snapshot.child("HeartRate").getValue().toString());
                spo2.setText(snapshot.child("SPO2").getValue().toString());
                System.out.println("sdsdsdsdddsds222@@@@@@@@@@@@@@@@");
                // This Will not give repeating data
                list.clear();
//                for (DataSnapshot dataSnapshot : snapshot.getChildren()){
//                    Model model = dataSnapshot.getValue(Model.class);
//                    list.add(model);
//                }
//                adapter.notifyDataSetChanged();
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });

        moveTempDataBtn.setOnClickListener(v -> {

        });
    }

}