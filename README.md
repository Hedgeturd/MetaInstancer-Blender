# MetaInstancer-Blender
This Addon can Import and Export MTI data for Hedgehog Engine 1.
> [!NOTE]
> This Addon is NOT perfect at the moment so
> - There are some issues with exporting rotations.<br>
> - The Import function is practically useless.

## To Do
- Add Cloud Instance Support

## Basic Setup Guide
### Scene Setup
To begin, make a surface which has a Particle System set on it.<br>
Use these settings:<br>
<img alt="ParticleType" height="200" src="tutorial/ParticleSettings1.png"/><br>

For some added randomness, I personally prefer using the settings below.<br>
Take note here that "Hair Length" is 4 metres, ONLY USE THIS VALUE FOR PREVIEWING!!!<br>
<img alt="EmissionRandom" src="tutorial/ParticleSettings2.png" width="334"/>
<img alt="RotationRandom" src="tutorial/ParticleSettings3.png" width="334"/>

### Painting
If you want more control over the placement you can add weight paints to the Particle Settings, follow below.<br>
"Group" being the vertex group I will be using to paint grass onto my surface<br>
<img alt="RotationRandom" src="tutorial/ParticleSettings4.png" width="323"/><br>
<br>
Then you can just begin painting your canvas like so:<br>
<img alt="WeightsPreview" src="tutorial/ScenePaint.png" width="460"/>

### Exporting
Once you're ready to export, make sure to go back to your Particle Emission Settings and reduce the Hair Length to 0.<br>
Then go to File > Export > Meta Instancer (.mti) and finally name and export your MTI.