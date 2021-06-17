//
//	This code was written by Ariel Dolan
//	Site	http://www.aridolan.com
//	Email	aridolan@netvision.net.il
//
//	You are welcome to do whatever you wish with this code, as long as you
//	add appropriate credits.
//

//package Gfloys;

import java.awt.*;

final class GfloyControl extends Frame {
    Button cancel;
    Button ok;
    Button reset;
	Button defaults;
	Button leader;
    Gfloy floys[];
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
	Choice color;
	Choice floynum;
	Label label;

    
    public GfloyControl (Gfloy f[]) {
        super("Floy Control Panel");
        floys = f;
		float fi = 0f;
        
        cancel = new Button("Cancel");
        ok = new Button("OK");
        reset = new Button("Reset");
		defaults = new Button("Defaults");
		leader = new Button("Leader");
        Panel okPanel = new Panel();
        okPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 15, 15));
        okPanel.add(cancel);
        okPanel.add(ok);
        okPanel.add(reset);
		okPanel.add(defaults);
		//okPanel.add(leader);
        this.add("South", okPanel);
        
		label = new Label("Properties (Global / Individual)");
        Panel titlePanel = new Panel();
        titlePanel.setLayout(new FlowLayout(FlowLayout.CENTER, 5, 5));
        titlePanel.add(label);
        this.add("North", titlePanel);
        //label.setText("f0 = "+f[0].acc+" floys0 = "+floys[0].acc);

        nf = new Choice();
        for (int i = 5; i <= 100; i += 5)
            nf.addItem(Integer.toString(i));
        nf.select(Integer.toString(Gfloys.NF));
        
        floynum = new Choice();
		floynum.addItem("All");
		floynum.addItem("Stranger");
        for (int i = 1; i <= 10; i++)
            floynum.addItem(Integer.toString(i));
        floynum.select("All");

		color = new Choice();
		color.addItem("BLACK");
		color.addItem("BLUE");
		color.addItem("CYAN");
		color.addItem("DARKGRAY");
		color.addItem("GRAY");
		color.addItem("GREEN");
		color.addItem("LIGHTGRAY");
		color.addItem("MAGENTA");
        color.addItem("ORANGE");
		color.addItem("PINK");
		color.addItem("RED");
		color.addItem("WHITE");
		color.addItem("YELLOW");

		color.select("GREEN");


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
        controlPanel.setLayout(new GridLayout(12, 2, 0, 0)); // 12 rows, 2 columns, 0 horizontal, 5 verticle
        controlPanel.add(new Label("Number of Floys:"));
		controlPanel.add(nf);
        controlPanel.add(new Label("Delay:"));         
		controlPanel.add(sleep);
        controlPanel.add(new Label("Free Will Factor:"));      
		controlPanel.add(kick);
		controlPanel.add(new Label("Number of Neighbors:"));      
		controlPanel.add(numnb);

		controlPanel.add(new Label("-----------",Label.CENTER));
		controlPanel.add(new Label("-----------",Label.CENTER));

        controlPanel.add(new Label("Applies to Floy No.:"));
		controlPanel.add(floynum);
        controlPanel.add(new Label("Floy Color:"));
		controlPanel.add(color);
        controlPanel.add(new Label("Acceleration:"));      
		controlPanel.add(acc);
        controlPanel.add(new Label("Adhesion:"));     
		controlPanel.add(acctomid);
        controlPanel.add(new Label("Collision Distance:"));    
		controlPanel.add(revdist);
        controlPanel.add(new Label("Max. Speed:"));	
		controlPanel.add(maxspeed);
        controlPanel.add(new Label("Bounce Speed:"));       
		controlPanel.add(bouncespeed);
		
		

        //controlPanel.add(new Label("Test:"));        
		//controlPanel.add(new Label(Long.toString(Gfloys.NF)));
        Panel alignPanel = new Panel();
        alignPanel.setLayout(new FlowLayout(FlowLayout.CENTER, 5, 5));
        alignPanel.add("Center", controlPanel);
        this.add("Center", alignPanel);
        
        this.pack();
        this.show();
        }
    

	private void reset(int num) {

		if (num == 1) {
	        nf.select(Integer.toString(Gfloys.NF));
			floynum.select("All");
		    acc.select(Float.toString((float) Gfloys.ACC));
			acctomid.select(Float.toString((float) Gfloys.ACCTOMID));
	        revdist.select(Integer.toString(Gfloys.REVDIST));
		    maxspeed.select(Float.toString((float) Gfloys.MAXSPEED));
			bouncespeed.select(Float.toString((float) Gfloys.BOUNCESPEED));
	        sleep.select(Integer.toString(Gfloys.SLEEP));
		    color.select("Green");
			kick.select(Float.toString((float) Gfloys.KICK));
			numnb.select(Integer.toString(Gfloys.NUMNB));
		}
		else {
	        nf.select(Integer.toString(10));
			floynum.select("All");
		    acc.select(Float.toString((float) 0.3));
			acctomid.select(Float.toString((float) 0.1));
	        revdist.select(Integer.toString(200));
		    maxspeed.select(Float.toString((float) 5));
			bouncespeed.select(Float.toString((float) 0.8));
	        sleep.select(Integer.toString(10));
		    color.select("Green");
			kick.select(Float.toString((float) 0.05));
			numnb.select(Integer.toString(2));
		}


	}

    public boolean action(Event e, Object arg) {

		String fnum;
		int num;
		int n;
		boolean flag = true;

        if (e.target == reset) {
			reset(1);
			}
        if (e.target == defaults) {
            Gfloys.reset();
			reset(1);
			}
        if (e.target == ok) {
			fnum = readString(floynum, "All");
			if (fnum.equals("All")) {
				Gfloys.ResetPopulation = true;
	            Gfloys.NF = readInt(nf, Gfloys.NF);
				Gfloys.ACC = readFloat(acc, Gfloys.ACC);
				Gfloys.ACCTOMID = readFloat(acctomid, Gfloys.ACCTOMID);
				Gfloys.REVDIST = readInt(revdist, Gfloys.REVDIST);
				Gfloys.MAXSPEED = readFloat(maxspeed, Gfloys.MAXSPEED);
				Gfloys.BOUNCESPEED = readFloat(bouncespeed, Gfloys.BOUNCESPEED);
				Gfloys.SLEEP = readInt(sleep, Gfloys.SLEEP);
				Gfloys.COLOR = readString(color, Gfloys.COLOR);
				Gfloys.KICK = readFloat(kick, Gfloys.KICK);
				Gfloys.NUMNB = readInt(numnb, Gfloys.NUMNB);
			}
			else {
				Gfloys.ResetPopulation = false;
				if (fnum.equals("Stranger"))
					num = 0;
				else { 
					n = Integer.parseInt(fnum);
					if (n > Gfloys.NF) {
						//Gfloys.beep.play();
						num = 1;
					}
					else {
						num = n;

						floys[num].acc = readFloat(acc, floys[num].acc);
						floys[num].acctomid = readFloat(acctomid, floys[num].acctomid);
						floys[num].revdist = readInt(revdist, floys[num].revdist);
						floys[num].maxspeed = readFloat(maxspeed, floys[num].maxspeed);
						floys[num].bouncespeed = readFloat(bouncespeed, floys[num].bouncespeed);
						floys[num].color = readColor(color, floys[num].GetColorName());
						//floys[num].color = GetColorByString(color.getSelectedItem());
						//floys[num].kick = readFloat(kick, floys[num].kick);
						floys[num].numnb = readInt(numnb, floys[num].numnb);
						if (floys[num].color == Color.red) 
							floys[num].type = 1;
						else
							floys[num].type = 0;
					}
				}
			}

            this.hide();
            this.dispose();
			Gfloys.First = true;
            return true;
            }
        if (e.target == cancel) {
			Gfloys.First = true;
            this.hide();
            this.dispose();
            return true;
            }
		
		
		if (e.target == nf) {
			Gfloys.NF = readInt(nf, Gfloys.NF);
			/*
			floynum = new Choice();
			floynum.addItem("All");
			floynum.addItem("Stranger");
			for (int i = 1; i <= Gfloys.NF; i++)
				floynum.addItem(Integer.toString(i));
			floynum.select("All");
			*/
		}
		

		if (e.target == floynum) {

			fnum = readString(floynum, "All");
			if (!fnum.equals("All")) {
				if (fnum.equals("Stranger"))
					num = 0;
				else {
					n = Integer.parseInt(fnum);
					if (n > Gfloys.NF) {
						Gfloys.beep.play();
						num = 1;
					}
					else {
						num = n;

						acc.select(Float.toString((float) floys[num].acc));
						acctomid.select(Float.toString((float) floys[num].acctomid));
						revdist.select(Float.toString((float) floys[num].revdist));
						maxspeed.select(Float.toString((float) floys[num].maxspeed));
						bouncespeed.select(Float.toString((float) floys[num].bouncespeed));
						color.select(floys[num].GetColorName());
						//kick.select(Float.toString((float) floys[num].kick));
						numnb.select(Integer.toString((int) floys[num].numnb));
					}
				}
			}

            return true;

		}
		
        else
            return false;
        }
    

    private String readString(Choice c, String d) {
        String n;
        
        try {
            n = c.getSelectedItem();
            }
        catch (Exception e) {
            n = d;
            }
        
        return n;
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



    private Color readColor(Choice c, String d) {
        String n;
		Color col;
        
        try {
            n = c.getSelectedItem();
            }
        catch (Exception e) {
            n = d;
            }
        
		col = GetColorByString(n);
        return col;

        }

	public Color GetColorByString(String c) {

		Color col;

		if (c.equals("BLACK")) col = Color.black;
		else if (c.equals("BLUE")) col = Color.blue;
		else if (c.equals("CYAN")) col = Color.cyan;
		else if (c.equals("DARKGRAY")) col = Color.darkGray;
		else if (c.equals("GRAY")) col = Color.gray;
		else if (c.equals("GREEN")) col = Color.green;
		else if (c.equals("LIGHTGRAY")) col = Color.lightGray;
		else if (c.equals("ORANGE")) col = Color.orange;
		else if (c.equals("PINK")) col = Color.pink;
		else if (c.equals("RED")) col = Color.red;
		else if (c.equals("WHITE")) col = Color.white;
		else if (c.equals("YELLOW")) col = Color.yellow;
		else col = Color.green;

		return col;

	}


}
