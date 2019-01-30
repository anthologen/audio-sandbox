// A ChucK program to sonify the Pythagorean comma

// Global Gain
Gain g => dac;
// set Gain (volume)
.5 => g.gain;

fun void playFreq( float freq, dur length )
{
    // connect to Gain
    //SinOsc s => g;
    TriOsc s => g;
    freq => s.freq;
    // advance time by length
    now + length => now;
    // disconnect the SinOsc
    s =< g;
}

fun void playSeries( float startingFreq, float freqRatio, int numIntervals, dur length )
{
    <<< startingFreq, freqRatio, numIntervals, length>>>;
    0 => int i;
    startingFreq => float freq;
    for (0 => i; i < numIntervals; i + 1 => i)
    {
        startingFreq * Math.pow(freqRatio, i) => freq;
        <<< i, freq >>>;
        playFreq(freq, length);
    }
}

fun void playSeriesBackwards( float targetFreq, float freqRatio, int numIntervals, dur length )
{
    <<< targetFreq, freqRatio, numIntervals, length>>>;
    0 => int i;
    targetFreq => float freq;
    for (0 => i; i < numIntervals; i + 1 => i)
    {
        targetFreq / Math.pow(freqRatio, i) => freq;
        <<< i, freq >>>;
        playFreq(freq, length);
    }
}


// parms
55.0 => float startingFreq; // A1
0.5::second => dur length;


3.0 / 2 => float p5ratio; // Perfect 5th
2 => float octaveRatio; // Octave


playSeries(startingFreq, p5ratio, 12, length);
playSeries(startingFreq, octaveRatio, 7, length);

now + 0.5::second => now;

Math.pow(p5ratio, 12) / Math.pow(octaveRatio, 7) => float pythagoreanComma;

playFreq(3520, 1::second);
now + 0.1::second => now;
playFreq(3520 * pythagoreanComma, 1::second);

now + 0.5::second => now;

0 => int i;
3 => int iterations;
for (0 => i; i < iterations; i + 1 => i)
{
    playFreq(440, 1::second);
    now + 0.1::second => now;
    playFreq(440 * pythagoreanComma, 1::second);
    now + 0.1::second => now;
}
