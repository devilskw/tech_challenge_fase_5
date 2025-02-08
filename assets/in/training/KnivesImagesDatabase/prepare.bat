cl@echo on
cd NEGATIVES_ALL
del /Q image_control.txt
for %%a in (*.bmp) DO echo %%a >> image_control.txt
COPY /Y *.bmp ..
cd ..
for /F %%a in (NEGATIVES_ALL/image_control.txt) DO ren %%a no-threat_%%a
cd POSITIVES_ALL
del /Q image_control.txt
for %%a in (*.bmp) DO echo %%a >> image_control.txt
COPY /Y *.bmp ..
cd ..
for /F %%a in (POSITIVES_ALL/image_control.txt) DO ren %%a threat_%%a
