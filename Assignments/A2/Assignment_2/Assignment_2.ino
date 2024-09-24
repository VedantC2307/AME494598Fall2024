#define LILYGO_WATCH_2019_WITH_TOUCH
#include <LilyGoWatch.h>

TTGOClass *ttgo;

void setup()
{
    Serial.begin(115200);
    ttgo = TTGOClass::getWatch();
    ttgo->begin();
    ttgo->openBL();

    ttgo->tft->fillScreen(TFT_WHITE);
    ttgo->tft->setTextColor(TFT_BLACK, TFT_WHITE);
    ttgo->tft->setTextFont(4);

    //Name
    String name = "VEDANT";

    // Calculate font height and width
    int16_t nameWidth = ttgo->tft->textWidth(name);
    int16_t nameHeight = ttgo->tft->fontHeight();

    //Calculate x and y position of name
    int16_t xPos = (ttgo->tft->width() - nameWidth) / 2;
    int16_t yPos = (ttgo->tft->height() - nameHeight) / 2;

    //Print name
    ttgo->tft->drawString(name,  xPos, yPos);
}

void loop()
{ 
}