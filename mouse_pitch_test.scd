// SuperCollider pitch modulation using mouse input test
{
        var x = SinOsc.ar(MouseX.kr(100, 200));
		var y = SinOsc.ar(MouseY.kr(100, 200));
        SinOsc.ar(440 * x + 800, 0, 0.5 )
	+ SinOsc.ar(880 * y + 800, 0, 0.5)
}.play;

s.boot