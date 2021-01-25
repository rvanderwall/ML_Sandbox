//
//	This code was written by Ariel Dolan
//	Site	http://www.aridolan.com
//	Email	aridolan@netvision.net.il
//
//	You are welcome to do whatever you wish with this code, as long as you
//	add appropriate credits.
//
//      Brings up a frame that allows user to change FLoy behavior
//
//package Floys;

import java.awt.*;

final class FloyControl extends Frame {

    private Button cancel;
    private Button ok;
    private Button reset;
    private Button defaults;
     
    private Choice numFloys;
    private Choice acceleration;
    private Choice centerAttraction;
    private Choice minDistance;
    private Choice maxSpeed;
    private Choice bounceSpeed;
    private Choice sleep;
    private Choice initSpeed;
    private Choice kick;
    private Choice numNeighbors;
    
    

    public FloyControl (Floy f[]) {        
        super("Floy Control");
        
        float fi;       // Temp used to populate lists
        
        cancel = new Button("Cancel");
        ok = new Button("OK");
        reset = new Button("Reset");
	defaults = new Button("Defaults");
        
        Panel okPanel = new Panel();
        okPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 15, 15));
        okPanel.add(cancel);
        okPanel.add(ok);
        okPanel.add(reset);
	okPanel.add(defaults);
        this.add("South", okPanel);
        
        Panel titlePanel = new Panel();
        titlePanel.setLayout(new FlowLayout(FlowLayout.CENTER, 15, 15));
        titlePanel.add(new Label("Floy Properties"));
        this.add("North", titlePanel);

        
        // How many Floys in the playing Field
        numFloys = new Choice();
        for (int i = 5; i <= 100; i += 5) {
            numFloys.addItem(Integer.toString(i));
        }
        numFloys.select(Integer.toString(FloyField.DEFAULT_NUM_FLOYS));
        
        acceleration = new Choice();
        acceleration.addItem(Float.toString((float) 0.05));
        for (int i = 1; i <= 10; i++) {
 	    fi = ((float) i)/10;
            acceleration.addItem(Float.toString(fi));
	}
        acceleration.select(Float.toString(Floy.DEFAULT_ACCELERATION));
        
        centerAttraction = new Choice();
	centerAttraction.addItem(Float.toString((float) 0.01));
        for (int i = 3; i <= 20; i += 2) {
	    fi = ((float) i)/100;
            centerAttraction.addItem(Float.toString(fi));
	}
        centerAttraction.select(Float.toString(Floy.DEFAULT_ATTRACTION_TO_CENTER));
        
        minDistance = new Choice();
        for (int i = 25; i <= 400; i *= 2) {
            minDistance.addItem(Integer.toString(i));
        }
        minDistance.select(Integer.toString(Floy.DEFAULT_MIN_DISTANCE));
        
        maxSpeed = new Choice();
        for (int i = 1; i <= 10; i++) {
            fi = ((float) i);
            maxSpeed.addItem(Float.toString(fi));
	}
        maxSpeed.select(Float.toString(Floy.DEFAULT_MAX_SPEED));
        
        bounceSpeed = new Choice();
        for (int i = 1; i <= 20; i *= 2) {
	    fi = ((float) i)/10;
            bounceSpeed.addItem(Float.toString(fi));
	}
        bounceSpeed.select(Float.toString(Floy.DEFAULT_BOUNCE_SPEED));
        
        sleep = new Choice();
        for (int i = 2; i <= 10; i += 1)
            sleep.addItem(Integer.toString(i));
        for (int i = 20; i <= 200; i += 10)
            sleep.addItem(Integer.toString(i));
        sleep.select(Integer.toString(FloyField.DEFAULT_INTERVAL_STEP));

	initSpeed = new Choice();
        for (int i = 1; i <= 10; i++) {
	    fi = ((float) i);
            initSpeed.addItem(Float.toString(fi));
	}
        initSpeed.select(Float.toString(Floy.DEFAULT_INITIAL_SPEED));

	kick = new Choice();
        for (int i = 1; i <= 20; i += 2) {
	    fi = ((float) i)/100;
            kick.addItem(Float.toString(fi));
	}
        kick.select(Float.toString((float) 0.05));

        
	numNeighbors = new Choice();
        for (int i = 1; i <= 10; i++)
            numNeighbors.addItem(Integer.toString(i));
        numNeighbors.select(Integer.toString(Floy.DEFAULT_NUM_NEIGHBORS));

	useCurValues();

        Panel controlPanel = new Panel();
        controlPanel.setLayout(new GridLayout(10, 2, 0, 5)); // 10 rows, 2 columns, 0 horizontal, 5 verticle
        controlPanel.add(new Label("Number of Floys:"));
		controlPanel.add(numFloys);
        controlPanel.add(new Label("Acceleration:"));      
		controlPanel.add(acceleration);
        controlPanel.add(new Label("Attraction to Center:"));     
		controlPanel.add(centerAttraction);
        controlPanel.add(new Label("Collision Distance:"));    
		controlPanel.add(minDistance);
        controlPanel.add(new Label("Max. Speed:"));		
		controlPanel.add(maxSpeed);
        controlPanel.add(new Label("Bounce Speed:"));       
		controlPanel.add(bounceSpeed);
        controlPanel.add(new Label("Delay:"));         
		controlPanel.add(sleep);
        controlPanel.add(new Label("Initial Speed:"));        
		controlPanel.add(initSpeed);
        controlPanel.add(new Label("Free Will Factor:"));      
		controlPanel.add(kick);
	controlPanel.add(new Label("Neighbors:"));      
		controlPanel.add(numNeighbors);

        Panel alignPanel = new Panel();
        alignPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 5, 5));
        alignPanel.add("Center", controlPanel);
        this.add("Center", alignPanel);
        
        this.pack();
        this.show();
    }
    

    private void useCurValues() {
            FloyField theField = FloyField.getInstance();
            numFloys.select(Integer.toString(theField.NumFloys));
	    acceleration.select(Float.toString(Floy.Generic_Acceleration));
	    centerAttraction.select(Float.toString(Floy.Generic_Attraction_To_Center));
	    minDistance.select(Integer.toString(Floy.Generic_Min_Distance));
            maxSpeed.select(Float.toString(Floy.Generic_Max_Speed));
	    bounceSpeed.select(Float.toString(Floy.Generic_Bounce_Speed));
	    sleep.select(Integer.toString(theField.SleepTime));
	    initSpeed.select(Float.toString(Floy.Generic_Initial_Speed));
	    kick.select(Float.toString((float) Floy.Generic_Free_Will));
	    numNeighbors.select(Integer.toString(Floy.Generic_Num_Neighbors));
    }


    public boolean action(Event e, Object arg) {
        FloyField theField = FloyField.getInstance();
        if (e.target == reset) {
	    useCurValues();
	}
        if (e.target == defaults) {
            theField.useDefaults();
            Floy.resetToDefaults();
	    useCurValues();
	}
        if (e.target == ok) {
            theField.useDefaults();
            theField.NumFloys = readInt(numFloys, theField.NumFloys);
	    Floy.Generic_Acceleration = readFloat(acceleration, Floy.Generic_Acceleration);
	    Floy.Generic_Attraction_To_Center = readFloat(centerAttraction, Floy.Generic_Attraction_To_Center);
	    Floy.Generic_Min_Distance = readInt(minDistance, Floy.Generic_Min_Distance);
	    Floy.Generic_Max_Speed = readFloat(maxSpeed, Floy.Generic_Max_Speed);
	    Floy.Generic_Bounce_Speed = readFloat(bounceSpeed, Floy.Generic_Bounce_Speed);
	    theField.SleepTime = readInt(sleep, theField.SleepTime);
	    Floy.Generic_Initial_Speed = readFloat(initSpeed, Floy.Generic_Initial_Speed);
	    Floy.Generic_Free_Will = readFloat(kick, Floy.Generic_Free_Will);
	    Floy.Generic_Num_Neighbors = readInt(numNeighbors, Floy.Generic_Num_Neighbors);
            this.hide();
            this.dispose();
            return true;
        }
        if (e.target == cancel) {
            this.hide();
            this.dispose();
            return true;
        }
        else
            return false;
    }

    
    
    
    private int readInt(Choice c, int d) {
        int n;
        
        try {
            n = Integer.parseInt(c.getSelectedItem());
        }
        catch (NumberFormatException e) {
            n = d;
        }    
        return n;
    }

    private float readFloat(Choice c, float d) {
        float n;
        
        try {
            n = Float.valueOf(c.getSelectedItem()).floatValue();
        }
        catch (NumberFormatException e) {
            n = d;
        }
        return n;
    }
}
