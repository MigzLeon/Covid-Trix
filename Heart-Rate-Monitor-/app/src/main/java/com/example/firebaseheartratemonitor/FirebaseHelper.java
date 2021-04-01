package com.example.firebaseheartratemonitor;
import androidx.annotation.NonNull;

import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.ArrayList;
import java.util.List;
public class FirebaseHelper {
    private FirebaseDatabase mDatabase;
    private DatabaseReference mReferencenSensors;
    private List<Sensor> sensors =  new ArrayList<>();

    public interface DataStatus{
        void DataIsLoaded(List<Sensor> sensors, List<String> Keys);
        void DataIsInserted();
        void DataIsUpdated();
        void DataIsDeleted();
    }

    public FirebaseHelper(){
        mDatabase = FirebaseDatabase.getInstance();
        mReferencenSensors = mDatabase.getReference("sensors");
    }
    public void readSensors(final DataStatus dataStatus){
        mReferencenSensors.addValueEventListener(new ValueEventListener() {

            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                sensors.clear();
                List<String> keys = new ArrayList<>();

                for (DataSnapshot keynode : dataSnapshot.getChildren()){
                    keys.add(keynode.getKey());

                    Sensor sensor;
//                    sensor = keynode.getValue(Sensor.class);
//                    sensors.add(sensor);
                }
                dataStatus.DataIsLoaded(sensors,keys);
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });
    }



}
