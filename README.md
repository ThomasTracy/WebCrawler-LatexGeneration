# WebCrawler-LatexGeneration
The aim of this project is to generate a thesis-like PDF file, which consist of text&paragraphs, pictures, diagrams, equations and references.  
So that the first part of this project is to downloading all required data with web crawling from different source.
And the second task is to combine all the data randomly in a latex file.  
## Web Crawling
**RefCrawler**  
Crawling and downloading references from IEEE, the raw references will be saved in a txt file "References" for latter use  
**ImgCrawler**  
Crawling and dowloading images from [Baidu image](image.baidu.com) (Google's copyright protection is too strict). Multiprocessing will be used to accelerate the downloading. All Images will be saved to folder Images.  
**GraphicCrawler**  
Crawling and downloading diagrams from [Mathwork](https://www.mathworks.com/help/matlab/graphics.html). Due to different html structure will here not only Multiprocessing but also Asycio be used to make the downloading faster.  All diagramms will be saved to folder Graphics.  
**EquationCrawler**  
When we retrieve some mathematical concepts on Wikipedia, many mathematical formulas are often included in the search results. This crawler will parse randomly on Wikipedia and download all the equations until the desired quantity is reached. It is worth nothing that all equations on html skript of Wikipedia are written in latex form, which means we can directly use in latter latex-generation. Equations will be saved in txt Equation.  
**PDFPaser**  
The normal text and paragraphs we dont need to download from internet. Instead we can directly cut from real thesis. Paragraphs will be saved in txt Text  
## Latex Generation  
The generated PDF pages should be devided into two styles. The one called `good page` are those pages only with references. The ohter called `bad page` are those with more than one element(eg. diagrams, equations...). Thus these two different types of pages can be used to train a neural network classifier.  
**DataWashing**  
All text data need to be washed before write into latex. For example all special characters such as α, β need to be transformed in to latex form(/Alpha, /Beta...). Moreover datawanshing make paragraphs seemed more beautiful.  
**PDFGenerator**  
Finally all data will be randomly filled in a latex file. Toatally will 50000 `good page` and 50000 `bad paged` be generated


![](https://github.com/ThomasTracy/WebCrawler-LatexGeneration/blob/master/good_page.jpg "good page")
![](https://github.com/ThomasTracy/WebCrawler-LatexGeneration/blob/master/bad_page.jpg "bad page")
