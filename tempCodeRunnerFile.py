
    def probablity (self,x):
        probability_cdf = norm.cdf(x, loc=self.mean, scale=self.std)
        return probability_cdf

    def valuechange(self):
        self.ui.fig.clf()
        self.u.axes = self.ui.fig.gca()
        self.speed = self.ui.horizontalSlider.value()
        probability_pdf2 = norm.cdf(self.speed, loc=self.mean, scale=self.std)
        print("the probabilty of the velocity = ",probability_pdf2)
        self.ui.textEdit.setText(""+probability_pdf2)
        self.u.axes.plot(self.data,self.probability_cdf)  
        self.u.axes.vlines(self.mean, 0, self.probablity(self.mean), colors='k', linestyles='--')
        self.u.axes.vlines(self.speed, 0, self.probablity(self.speed), colors='r', linestyles='dotted',label='velocity')
        self.ui.image_canvas.draw() 
        self.ui.image_canvas.flush_events()

def main():
    app = QApplication(sys.argv)
    main = UI()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':      
 main()