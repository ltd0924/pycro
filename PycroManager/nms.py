
from pycromanager import Bridge
import peak


class nms:
    def __init__(self):
        self.peaks=[]
        bridge = Bridge()
        roi=bridge.construct_java_object("ij.gui.Roi")
        self.img=bridge.construct_java_object("ij.process.ImageProcessor")
        self.imgresult=bridge.construct_java_object("ij.process.ImageProcessor")
        self.roi=roi.__init__(0,0,10,10)


    def getN(self):
        return len(self.peaks)

    def img_run(self,im,n,cutoff):
        self.im_ = im
        self.width_ = im.getWidth()
        self.height_ = im.getHeight()
        self.img = im.getProcessor()
        self.imgresult = self.img.clone()
        self.imgresult.setValue(65535)
        self.n_ = n
        self.cutoff_ = cutoff;
        self.peaks.clear()
        return self.image_process()



    def image_process(self):
        width_=self.width_
        height_=self.height_
        n_=self.n_
        cutoff_=self.cutoff_
        for i in range(0,width_-n_-1,n_+1):
            for j in range(0,height_-n_-1,n_+1):
                mi=i
                mj=j
                for ii in range(i,i+n_):
                    for jj in range(j,j+n_):
                        if self.img.get(ii,jj)> self.img.get(mi,mj):
                            mi=ii
                            mj=jj
                failed=False

                for ll in range(mi-n_,mi+n_):
                    for kk in range(mj-n_,mj+n_):
                        if (ll<i or ll>i+n_) | (kk<j or kk>j+n_):
                            if (ll<width_ and ll>0 ) & (kk<height_ and kk>0):
                                failed=True
                                break
                if ~failed:
                    if self.img.get(mi,mj)>cutoff_:
                        self.peaks.append(peak.__init__(mi,mj,self.img.get(mi,mj)))

        for k in self.peaks:
            mi=k.getX()
            mj=k.getY()
            self.roi.set_location(mi-5,mj-5)
            self.imgresult.draw(self.roi)

        self.imgresult.multipy(5)





