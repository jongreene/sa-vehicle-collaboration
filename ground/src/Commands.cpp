//
// Created by uberslam on 4/4/19.
//
#include "Commands.h"
#include "PlatformInterface.h"
using namespace std;

Commands::Commands(void* platform) {
	platform_ = (PlatformInterface*)platform;
	commands["drive"] = &Commands::Drive;
	commands["stop"] = &Commands::Stop;

	initMotorDriver();
}

#define TIMER_TOP                   100
#define PWM_INITIAL_DUTY_CYLCE      0
DigitalOut INT_A_1(PA12);
DigitalOut INT_A_2(PA14);
DigitalOut INT_B_1(PE1);
DigitalOut INT_B_2(PE3);
DigitalOut INT_C_1(PD2);
DigitalOut INT_C_2(PD4);
DigitalOut INT_D_1(PD7);
DigitalOut INT_D_2(PD8);
void Commands::initMotorDriver(){
	INT_A_1 = 0;
	INT_A_2 = 1;
	INT_B_1 = 0;
	INT_B_2 = 1;
	INT_C_1 = 0;
	INT_C_2 = 1;
	INT_D_1 = 0;
	INT_D_2 = 1;

	//Common pwm settings
	// Create the timer count control object initializer
	TIMER_InitCC_TypeDef timerCCInit = TIMER_INITCC_DEFAULT;
	timerCCInit.mode = timerCCModePWM;
	timerCCInit.cmoa = timerOutputActionToggle;
    CMU_ClockEnable(cmuClock_GPIO, true);
	// Create a timerInit object, based on the API default
	TIMER_Init_TypeDef timerInit = TIMER_INIT_DEFAULT;
	timerInit.prescale = timerPrescale16;

///////////////////////////////////////////////////////////////////////////
//////// timer0
///////////////////////////////////////////////////////////////////////////
	CMU_ClockEnable(cmuClock_TIMER0, true);

	// Enable Pin output
	GPIO_PinModeSet(gpioPortD, 3, gpioModePushPull, 0);

	// Configure CC channel 2
	TIMER_InitCC(TIMER0, 2, &timerCCInit);

	// Route CC2 to location 1 (PE3) and enable pin for cc2
	TIMER0->ROUTE |= (TIMER_ROUTE_CC2PEN | TIMER_ROUTE_LOCATION_LOC3);
	// Set Top Value
	TIMER_TopSet(TIMER0, TIMER_TOP);
	// Set the PWM duty cycle here!
	TIMER_CompareBufSet(TIMER0, 2, PWM_INITIAL_DUTY_CYLCE);

	TIMER_Init(TIMER0, &timerInit);

///////////////////////////////////////////////////////////////////////////
//////// timer1
///////////////////////////////////////////////////////////////////////////
	CMU_ClockEnable(cmuClock_TIMER1, true);

	// Enable Pin output
	GPIO_PinModeSet(gpioPortD, 6, gpioModePushPull, 0);

	// Configure CC channel 2
	TIMER_InitCC(TIMER1, 0, &timerCCInit);

	// Route CC2 to location 1 (PE3) and enable pin for cc2
	TIMER1->ROUTE |= (TIMER_ROUTE_CC0PEN | TIMER_ROUTE_LOCATION_LOC4);
	// Set Top Value
	TIMER_TopSet(TIMER1, TIMER_TOP);
	// Set the PWM duty cycle here!
	TIMER_CompareBufSet(TIMER1, 0, PWM_INITIAL_DUTY_CYLCE);

	timerInit.prescale = timerPrescale16;

	TIMER_Init(TIMER1, &timerInit);

///////////////////////////////////////////////////////////////////////////
//////// timer2
///////////////////////////////////////////////////////////////////////////
	CMU_ClockEnable(cmuClock_TIMER2, true);

	// Enable Pin output
	GPIO_PinModeSet(gpioPortA, 13, gpioModePushPull, 0);

	// Configure CC channel 2
	TIMER_InitCC(TIMER2, 1, &timerCCInit);

	// Route CC2 to location 1 (PE3) and enable pin for cc2
	TIMER2->ROUTE |= (TIMER_ROUTE_CC1PEN | TIMER_ROUTE_LOCATION_LOC1);
	// Set Top Value
	TIMER_TopSet(TIMER2, TIMER_TOP);
	// Set the PWM duty cycle here!
	TIMER_CompareBufSet(TIMER2, 1, PWM_INITIAL_DUTY_CYLCE);

	TIMER_Init(TIMER2, &timerInit);

///////////////////////////////////////////////////////////////////////////
//////// timer3
///////////////////////////////////////////////////////////////////////////
    CMU_ClockEnable(cmuClock_TIMER3, true);

    // Enable Pin output
	GPIO_PinModeSet(gpioPortE, 2, gpioModePushPull, 0);
	GPIO_PortOutClear(gpioPortE, 2);

    // Configure CC channel 2
    TIMER_InitCC(TIMER3, 2, &timerCCInit);

    // Route CC2 to location 1 (PE3) and enable pin for cc2
    TIMER3->ROUTE |= (TIMER_ROUTE_CC2PEN | TIMER_ROUTE_LOCATION_LOC1);
    // Set Top Value
    TIMER_TopSet(TIMER3, TIMER_TOP);
    // Set the PWM duty cycle here!
    TIMER_CompareBufSet(TIMER3, 2, PWM_INITIAL_DUTY_CYLCE);

    TIMER_Init(TIMER3, &timerInit);
}

int Commands::Drive(const vector<string> &parameters) {
	string message = "Parameters: ";
	for(auto param : parameters)
		message += param += " ";
	print(message);


	if(parameters.at(1) == "four_wheel") {
		if(parameters.size()<6){
			message = "wrong number of params";
			print(message);
			return -1;
		}
		core_util_critical_section_enter();
		TIMER_CompareBufSet(TIMER0, 2, stoi(parameters.at(2)));
		TIMER_CompareBufSet(TIMER1, 0, stoi(parameters.at(3)));
		TIMER_CompareBufSet(TIMER2, 1, stoi(parameters.at(4)));
		TIMER_CompareBufSet(TIMER3, 2, stoi(parameters.at(5)));
		core_util_critical_section_exit();
	}
	else if(parameters.at(1) == "two_wheel"){
		if(parameters.size()<4){
			message = "wrong number of params";
			print(message);
			return -1;
		}
		core_util_critical_section_enter();
		TIMER_CompareBufSet(TIMER0, 2, stoi(parameters.at(2)));
		TIMER_CompareBufSet(TIMER1, 0, stoi(parameters.at(2)));
		TIMER_CompareBufSet(TIMER2, 1, stoi(parameters.at(3)));
		TIMER_CompareBufSet(TIMER3, 2, stoi(parameters.at(3)));
		core_util_critical_section_exit();
	}

	return 0;
}

int Commands::Stop() {
	core_util_critical_section_enter();
	TIMER_CompareBufSet(TIMER0, 2, 0);
	TIMER_CompareBufSet(TIMER1, 0, 0);
	TIMER_CompareBufSet(TIMER2, 1, 0);
	TIMER_CompareBufSet(TIMER3, 2, 0);
	core_util_critical_section_exit();

}

int Commands::Stop(const vector<string> &parameters) {
	return Stop();
}

int Commands::executeCommand(vector<string>& parameters) {
	vector<string> local_parameters = parameters;
	string command = local_parameters.at(0);
	if(findCommand(command)) {
		return (this->*commands[command])(local_parameters);
	}

	return -1;
}

bool Commands::findCommand(string &command) {
	return commands.find(command) != commands.end();
}

void Commands::print(string str) {
	PlatformInterface* platform = (PlatformInterface*)platform_;
	platform->emit(str);
}



