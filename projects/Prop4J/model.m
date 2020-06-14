Prop4JSPL : [Operators] [Input_Output] [SatSolver] [To_CNF] [Tests] :: _Prop4JSPL ;

Operators : [And] [Or] [Implies] [Negation] [Equals] [extended] :: _Operators ;

extended : [AtLeast] [AtMost] [Choose] :: _extended ;

Input_Output : [Node_Reader] [Node_Writer] :: _Input_Output ;

%%

Operators implies And and Or and Negation ;
SatSolver implies To_CNF ;
To_CNF implies AtLeast and AtMost and Choose and Implies and Equals;
Tests implies To_CNF and Node_Reader and SatSolver ;
Node_Reader implies And and Or and Negation and Equals and Implies;
Node_Writer implies AtLeast and AtMost and Choose and Implies and Equals and And and Or and Negation;
Negation implies AtLeast and AtMost and And and Or;

