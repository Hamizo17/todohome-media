import numpy as np, soundfile as sf, sys
sr=48000; D=float(sys.argv[1]); ST=[float(x) for x in sys.argv[2].split(",")]; OUT=sys.argv[3]; n=int(D*sr); bpm=128; beat=60/bpm
out=np.zeros(n); rng=np.random.default_rng(3)
def add(sig,start,g=1):
    i=int(start*sr)
    if i>=n or i<0: return
    j=min(n,i+len(sig)); out[i:j]+=g*sig[:j-i]
def env(L,a=.002,d=.2):
    x=np.arange(int(L*sr))/sr; return np.minimum(1,x/a)*np.exp(-x/d)
K=np.tanh(2.2*np.sin(2*np.pi*np.cumsum(48+160*np.exp(-np.arange(int(.4*sr))/sr/.03))/sr))*env(.4,.0005,.16)
def hat(o=False): L=.18 if o else .05; return np.diff(rng.standard_normal(int(L*sr)+1))*env(L,.0003,.06 if o else .012)
clap=lambda: rng.standard_normal(int(.2*sr))*env(.2,.001,.05)
def acid(f,L,cut):
    x=np.arange(int(L*sr))/sr; ph=(f*x)%1; saw=2*ph-1
    y=np.zeros_like(saw); a=0
    for i in range(len(saw)):
        a+= cut*(saw[i]-a); y[i]=a
    return np.tanh(3*y)*env(L,.002,.12)
# patrón acid en La menor
PAT=[55,55,110,55,65.4,55,82.4,55, 55,110,55,98,55,65.4,73.4,55]
nb=int(D/beat)+2; step=beat/4
for b in range(nb):
    st=b*beat; brk=ST[3]-.1<=st<ST[3]+.8; intro=st<2.5
    if not brk: add(K,st,1.0 if not intro else .7)
    if not intro and not brk: add(hat(True),st+beat/2,.28)
    for s in range(4):
        add(hat(),st+s*step,.18 if s%2 else .1)
    if b%2==1 and not intro: add(clap(),st,.45)
    if not intro:
        for s in range(4):
            idx=(b*4+s)%16; cut=.05+.12*(0.5+0.5*np.sin(2*np.pi*(st+s*step)/8))
            add(acid(PAT[idx],step*.9,cut),st+s*step,.32)
# subida de ruido antes de los golpes y crashes
for s in [ST[1],ST[3]+.9,ST[5],ST[6]]:
    w=rng.standard_normal(int(1.0*sr)); add(w*np.linspace(0,1,len(w))**3*.35,s-1.0)
    add(rng.standard_normal(int(1.2*sr))*env(1.2,.001,.4)*.25,s)
    add(np.sin(2*np.pi*np.cumsum(np.linspace(120,35,int(.7*sr)))/sr)*env(.7,.001,.3),s,.9)
out/=np.max(np.abs(out)); sf.write(OUT,out,sr); print("ok")
