//
//	This code was written by Ariel Dolan
//	Site	http://www.aridolan.com
//	Email	aridolan@netvision.net.il
//
//	You are welcome to do whatever you wish with this code, as long as you
//	add appropriate credits.
//

//package Floys;

import java.awt.*;

final class FloyControl extends Frame {
    Button cancel;
    Button ok;
    Button reset;
	Button defaults;
    Floy floys[];
    Choice nf;
    Choice acc;
    Choice acctomid;
	Choice revdist;
    Choice maxspeed;
    Choice bouncespeed;
    Choice sleep;
    Choice v0;
    Choice kick;
	Choice numnb;
    
    public FloyControl (Floy f[]) {
        super("Floy Control");
        floys = f;
		float fi = 0f;
        
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
        
        nf = new Choice();
        for (int i = 5; i <= 100; i += 5)
            nf.addItem(Integer.toString(i));
        nf.select(Integer.toString(Floys.NF));
        
        acc = new Choice();
        acc.addItem(Float.toString((float) 0.05));
        for (int i = 1; i <= 10; i++) {
			fi = ((float) i)/10;
            acc.addItem(Float.toString(fi));
		}
        acc.select(Float.toString((float) 0.3));
        
        acctomid = new Choice();
		//acctomid.addItem(Float.toString((float) 0.05));
        for (int i = 2; i <= 20; i += 2) {
			fi = ((float) i)/100;
            acctomid.addItem(Float.toString(fi));
		}
        acctomid.select(Float.toString((float) 0.1));
        
        revdist = new Choice();
        for (int i = 25; i <= 400; i *= 2)
            revdist.addItem(Integer.toString(i));
        revdist.select(Integer.toString(200));
        
        maxspeed = new Choice();
        for (int i = 1; i <= 10; i++) {
			fi = ((float) i);
            maxspeed.addItem(Float.toString(fi));
		}
        maxspeed.select(Float.toString((float) 5.0));
        
        bouncespeed = new Choice();
        for (int i = 1; i <= 20; i *= 2) {
			fi = ((float) i)/10;
            bouncespeed.addItem(Float.toString(fi));
		}
        bouncespeed.select(Float.toString((float) 0.8));
        
        sleep = new Choice();
        for (int i = 2; i <= 10; i += 1)
            sleep.addItem(Integer.toString(i));
        for (int i = 20; i <= 200; i += 10)
            sleep.addItem(Integer.toString(i));
        sleep.select(Integer.toString(10));

		v0 = new Choice();
        for (int i = 1; i <= 10; i++) {
			fi = ((float) i);
            v0.addItem(Float.toString(fi));
		}
        v0.select(Float.toString((float) 4.0));

		kick = new Choice();
        for (int i = 1; i <= 10; i += 2) {
			fi = ((float) i)/100;
            kick.addItem(Float.toString(fi));
		}
        kick.select(Float.toString((float) 0.05));

		numnb = new Choice();
        for (int i = 1; i <= 10; i++)
            numnb.addItem(Integer.toString(i));
        numnb.select(Integer.toString(2));

		reset(1);

        Panel controlPanel = new Panel();
        controlPanel.setLayout(new GridLayout(10, 2, 0, 5)); // 10 rows, 2 columns, 0 horizontal, 5 verticle
        controlPanel.add(new Label("Number of Floys:"));
		controlPanel.add(nf);
        controlPanel.add(new Label("Acceleration:"));      
		controlPanel.add(acc);
        controlPanel.add(new Label("Attrcation to Center:"));     
		controlPanel.add(acctomid);
        controlPanel.add(new Label("Collision Distance:"));    
		controlPanel.add(revdist);
        controlPanel.add(new Label("Max. Speed:"));		
		controlPanel.add(maxspeed);
        controlPanel.add(new Label("Bounce Speed:"));       
		controlPanel.add(bouncespeed);
        controlPanel.add(new Label("Delay:"));         
		controlPanel.add(sleep);
        controlPanel.add(new Label("Initial Speed:"));        
		controlPanel.add(v0);
        controlPanel.add(new Label("Free Will Factor:"));      
		controlPanel.add(kick);
		controlPanel.add(new Label("Neighbors:"));      
		controlPanel.add(numnb);
        //controlPanel.add(new Label("Test:"));        
		//controlPanel.add(new Label(Long.toString(Floys.NF)));
        Panel alignPanel = new Panel();
        alignPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 5, 5));
        alignPanel.add("Center", controlPanel);
        this.add("Center", alignPanel);
        
        this.pack();
        this.show();
        }
    

	private void reset(int num) {

		if (num == 1) {
	        nf.select(Integer.toString(Floys.NF));
		    acc.select(Float.toString((float) Floys.ACC));
			acctomid.select(Float.toString((float) Floys.ACCTOMID));
	        revdist.select(Integer.toString(Floys.REVDIST));
		    maxspeed.select(Float.toString((float) Floys.MAXSPEED));
			bouncespeed.select(Float.toString((float) Floys.BOUNCESPEED));
	        sleep.select(Integer.toString(Floys.SLEEP));
		    v0.select(Float.toString((float) Floys.V0));
			kick.select(Float.toString((float) Floys.KICK));
			numnb.select(Integer.toString(Floys.NUMNB));
		}
		else {
	        nf.select(Integer.toString(10));
		    acc.select(Float.toString((float) 0.3));
			acctomid.select(Float.toString((float) 0.1));
	        revdist.select(Integer.toString(200));
		    maxspeed.select(Float.toString((float) 5));
			bouncespeed.select(Float.toString((float) 0.8));
	        sleep.select(Integer.toString(10));
		    v0.select(Float.toString((float) 4));
			kick.select(Float.toString((float) 0.05));
			numnb.select(Integer.toString(2));
		}


	}

    public boolean action(Event e, Object arg) {
        if (e.target == reset) {
			reset(1);
			}
        if (e.target == defaults) {
            Floys.reset();
			reset(1);
			}
        if (e.target == ok) {
            Floys.NF = readInt(nf, Floys.NF);
			Floys.ACC = readFloat(acc, Floys.ACC);
			Floys.ACCTOMID = readFloat(acctomid, Floys.ACCTOMID);
			Floys.REVDIST = readInt(revdist, Floys.REVDIST);
			Floys.MAXSPEED = readFloat(maxspeed, Floys.MAXSPEED);
			Floys.BOUNCESPEED = readFloat(bouncespeed, Floys.BOUNCESPEED);
			Floys.SLEEP = readInt(sleep, Floys.SLEEP);
			Floys.V0 = readFloat(v0, Floys.V0);
			Floys.KICK = readFloat(kick, Floys.KICK);
			Floys.NUMNB = readInt(numnb, Floys.NUMNB);

            this.hide();
            this.dispose();
			Floys.First = true;
            return true;
            }
        if (e.target == cancel) {
			Floys.First = true;
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
