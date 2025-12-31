//
// Basics
//

#define GREY(g)  g g g
#define black    GREY(0.0)
#define white    GREY(1)

#define RED      1 0 0
#define red      #FF0000
#define GREEN    0 1 0
#define BLUE     0 0 1
#define CYAN     0 1 1
#define YELLOW   1 1 0
#define MAGENTA  1 0 1

#define PINK     1 0.8 0.8
#define MINT     0.8 1 0.8
#define LTBLUE   0.5 0.5 1
#define LTYELLOW 1 1 0.5
#define ORANGE   1 0.5 0
#define BROWN	 #8C6238

//
// New variables
//

#define BG_HI      #303132
#define BG_MED     #262626
#define BG_LO      #1E1E1F

#define SEL        GREY(0.5)
#define BORDER     SEL
#define DISABLED   GREY(0.2)

#define BUTTON     #404040

#define BEVEL_HI   GREY(0.52)
#define BEVEL_LO   black

#define SEP        #363738
#define ERR        1 0 0

#define TEXT       #ACDAD5
#define TEXT_DIM   GREY(0.5)

//
// Old variables
//

#define DRKBASE              GREY(0.179) // Textbox line number bg
#define DRKGRADHIGH          GREY(0.1)
#define DRKGRADLOW           #1F1F1F
#define WELL                 GREY(0.15)
#define LISTA                DRKBASE
#define LISTB                DRKGRADLOW
#define TOOLBAR              #1A0F00

#define UNK                  1 0 1

#define DARK                 GREY(0.2)
#define arrow                GREY(0.5)

#define SHADOW1_5            GREY(0.699)
#define SHADOW2              GREY(0.63)
#define SHADOW3              GREY(0.58)

#define PRESSED_HIGH         #4A5E73
#define PRESSED_LOW          #768EA7

#define SELECTION_BASE       #FF9600
#define SELECTION_HIGHLIGHT2 1 0.9 0.5
#define SELECTION_SHADOW     1 0.4 0

#define BUTTON_SEL           SELECTION_BASE
#define BUTTON_PRESS         SELECTION_BASE
#define BASE_ALT             GREY(0.151) // effect in spreadsheet

#define EMPTY                DRKBASE

#define TEXT_HIGHLIGHT       GREY(0.9)

#define EDIT_BG              GREY(0.075) // Textbox bg
#define EDIT_BG_HIGHLIGHT    GREY(0.18)  // Textbox border
#define EDIT_BG_OUTLINE      GREY(0.14)  // Textbox border
