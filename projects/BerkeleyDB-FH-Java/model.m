//Semantic Dependencies
SPL : [generatedSPL] :: _SPL ;

generatedSPL : DERIVATIVES* [Logging] ConcurrTrans Persistance [Statistics] BTree Ops [MemoryBudget] base :: _generatedSPL ;

DERIVATIVES : Derivative_LoggingEvictor_Statistics_Evictor_LoggingBase
	| Derivative_LoggingEvictor_Evictor_MemoryBudget_LoggingBase
	| Derivative_LoggingInfo_Statistics_Verifier
	| Derivative_Latches_Statistics_Verifier
	| Derivative_Latches_Verifier_INCompressor
	| Derivative_Statistics_Verifier_INCompressor
	| Derivative_Statistics_Verifier_DeleteOp
	| Derivative_LookAHEADCache_Evictor_CriticalEviction
	| Derivative_INCompressor_Evictor_CriticalEviction
	| Derivative_Evictor_MemoryBudget_CriticalEviction
	| Derivative_LoggingEvictor_Evictor_LoggingBase
	| Derivative_FSync_Latches
	| Derivative_NIO_ChunkedNIO
	| Derivative_IO_SynchronizedIO
	| Derivative_LoggingConfig_Statistics
	| Derivative_FSync_Statistics
	| Derivative_LookAHEADCache_Statistics
	| Derivative_Latches_Statistics
	| Derivative_Latches_CheckLeaks
	| Derivative_Statistics_CheckLeaks
	| Derivative_Statistics_Verifier
	| Derivative_LoggingFinest_CPBytes
	| Derivative_CheckpointerDaemon_CPBytes
	| Derivative_LoggingFinest_CPTime
	| Derivative_CPBytes_CPTime
	| Derivative_LoggingFine_INCompressor
	| Derivative_Latches_INCompressor
	| Derivative_Statistics_INCompressor
	| Derivative_Verifier_INCompressor
	| Derivative_LoggingCleaner_DeleteOp
	| Derivative_Latches_DeleteOp
	| Derivative_Statistics_DeleteOp
	| Derivative_INCompressor_DeleteOp
	| Derivative_LoggingFinest_TruncateOp
	| Derivative_Latches_TruncateOp
	| Derivative_DeleteOp_TruncateOp
	| Derivative_Latches_RenameOp
	| Derivative_LoggingEvictor_Evictor
	| Derivative_Latches_Evictor
	| Derivative_Statistics_Evictor
	| Derivative_INCompressor_Evictor
	| Derivative_DeleteOp_Evictor
	| Derivative_LoggingInfo_MemoryBudget
	| Derivative_LookAHEADCache_MemoryBudget
	| Derivative_Latches_MemoryBudget
	| Derivative_Statistics_MemoryBudget
	| Derivative_DeleteOp_MemoryBudget
	| Derivative_Evictor_MemoryBudget
	| Derivative_Evictor_CriticalEviction
	| Derivative_Evictor_EvictorDaemon
	| Derivative_Latches_FileHandleCache
	| Derivative_LoggingSevere_EnvironmentLocking
	| Derivative_LoggingFinest_LoggingBase
	| Derivative_LoggingFiner_LoggingBase
	| Derivative_LoggingFine_LoggingBase
	| Derivative_LoggingSevere_LoggingBase
	| Derivative_LoggingRecovery_LoggingBase
	| Derivative_LoggingCleaner_LoggingBase
	| Derivative_LoggingFileHandler_LoggingBase
	| Derivative_LoggingDbLogHandler_LoggingBase
	| Derivative_LoggingConsoleHandler_LoggingBase ;

Logging : [LoggingFiner] [LoggingConfig] [LoggingSevere] [LoggingEvictor] [LoggingCleaner] [LoggingRecovery] [LoggingDbLogHandler] [LoggingConsoleHandler] [LoggingInfo] LoggingBase [LoggingFileHandler] [LoggingFine] [LoggingFinest] :: _Logging ;

ConcurrTrans : [Latches] [Transactions] [CheckLeaks] [FSync] :: _ConcurrTrans ;

Persistance : [Checksum] IIO [EnvironmentLocking] Checkpointer [DiskFullErro] [FileHandleCache] IICleaner :: _Persistance ;

IIO : [SynchronizedIO] IO :: OldIO
	| NIOAccess [DirectNIO] :: NewIO ;

NIOAccess : ChunkedNIO
	| NIO ;

Checkpointer : [CPBytes] [CPTime] [CheckpointerDaemon] :: _Checkpointer ;

IICleaner : [CleanerDaemon] Cleaner [LookAHEADCache] :: _IICleaner ;

BTree : [INCompressor] [IEvictor] [Verifier] :: _BTree ;

IEvictor : [CriticalEviction] [EvictorDaemon] Evictor :: _IEvictor ;

Ops : [DeleteOp] [RenameOp] [TruncateOp] :: _Ops ;

%%

Evictor or EvictorDaemon or LookAHEADCache implies MemoryBudget ;
CriticalEviction implies INCompressor ;
CPBytes implies CPTime ;
DeleteOp implies Evictor and INCompressor and MemoryBudget ;
MemoryBudget implies Evictor and Latches ;
TruncateOp implies DeleteOp ;
Verifier implies INCompressor ;
Derivative_LoggingEvictor_Statistics_Evictor_LoggingBase iff LoggingBase and Evictor and Statistics and LoggingEvictor ;
Derivative_LoggingEvictor_Evictor_MemoryBudget_LoggingBase iff LoggingBase and Evictor and LoggingEvictor and MemoryBudget ;
Derivative_LoggingInfo_Statistics_Verifier iff Verifier and LoggingInfo and Statistics ;
Derivative_Latches_Statistics_Verifier iff Latches and Verifier and Statistics ;
Derivative_Latches_Verifier_INCompressor iff Latches and INCompressor and Verifier ;
Derivative_Statistics_Verifier_INCompressor iff INCompressor and Verifier and Statistics ;
Derivative_Statistics_Verifier_DeleteOp iff Verifier and Statistics and DeleteOp ;
Derivative_LookAHEADCache_Evictor_CriticalEviction iff Evictor and LookAHEADCache and CriticalEviction ;
Derivative_INCompressor_Evictor_CriticalEviction iff INCompressor and Evictor and CriticalEviction ;
Derivative_Evictor_MemoryBudget_CriticalEviction iff Evictor and CriticalEviction and MemoryBudget ;
Derivative_LoggingEvictor_Evictor_LoggingBase iff LoggingBase and Evictor and LoggingEvictor ;
Derivative_FSync_Latches iff Latches and FSync ;
Derivative_NIO_ChunkedNIO iff ChunkedNIO and NIO ;
Derivative_IO_SynchronizedIO iff IO and SynchronizedIO ;
Derivative_LoggingConfig_Statistics iff LoggingConfig and Statistics ;
Derivative_FSync_Statistics iff FSync and Statistics ;
Derivative_LookAHEADCache_Statistics iff LookAHEADCache and Statistics ;
Derivative_Latches_Statistics iff Latches and Statistics ;
Derivative_Latches_CheckLeaks iff Latches and CheckLeaks ;
Derivative_Statistics_CheckLeaks iff CheckLeaks and Statistics ;
Derivative_Statistics_Verifier iff Verifier and Statistics ;
Derivative_LoggingFinest_CPBytes iff CPBytes and LoggingFinest ;
Derivative_CheckpointerDaemon_CPBytes iff CPBytes and CheckpointerDaemon ;
Derivative_LoggingFinest_CPTime iff LoggingFinest and CPTime ;
Derivative_CPBytes_CPTime iff CPBytes and CPTime ;
Derivative_LoggingFine_INCompressor iff INCompressor and LoggingFine ;
Derivative_Latches_INCompressor iff Latches and INCompressor ;
Derivative_Statistics_INCompressor iff INCompressor and Statistics ;
Derivative_Verifier_INCompressor iff INCompressor and Verifier ;
Derivative_LoggingCleaner_DeleteOp iff LoggingCleaner and DeleteOp ;
Derivative_Latches_DeleteOp iff Latches and DeleteOp ;
Derivative_Statistics_DeleteOp iff Statistics and DeleteOp ;
Derivative_INCompressor_DeleteOp iff INCompressor and DeleteOp ;
Derivative_LoggingFinest_TruncateOp iff LoggingFinest and TruncateOp ;
Derivative_Latches_TruncateOp iff Latches and TruncateOp ;
Derivative_DeleteOp_TruncateOp iff TruncateOp and DeleteOp ;
Derivative_Latches_RenameOp iff Latches and RenameOp ;
Derivative_LoggingEvictor_Evictor iff Evictor and LoggingEvictor ;
Derivative_Latches_Evictor iff Latches and Evictor ;
Derivative_Statistics_Evictor iff Evictor and Statistics ;
Derivative_INCompressor_Evictor iff INCompressor and Evictor ;
Derivative_DeleteOp_Evictor iff Evictor and DeleteOp ;
Derivative_LoggingInfo_MemoryBudget iff LoggingInfo and MemoryBudget ;
Derivative_LookAHEADCache_MemoryBudget iff LookAHEADCache and MemoryBudget ;
Derivative_Latches_MemoryBudget iff Latches and MemoryBudget ;
Derivative_Statistics_MemoryBudget iff Statistics and MemoryBudget ;
Derivative_DeleteOp_MemoryBudget iff DeleteOp and MemoryBudget ;
Derivative_Evictor_MemoryBudget iff Evictor and MemoryBudget ;
Derivative_Evictor_CriticalEviction iff Evictor and CriticalEviction ;
Derivative_Evictor_EvictorDaemon iff Evictor and EvictorDaemon ;
Derivative_Latches_FileHandleCache iff Latches and FileHandleCache ;
Derivative_LoggingSevere_EnvironmentLocking iff LoggingSevere and EnvironmentLocking ;
Derivative_LoggingFinest_LoggingBase iff LoggingBase and LoggingFinest ;
Derivative_LoggingFiner_LoggingBase iff LoggingBase and LoggingFiner ;
Derivative_LoggingFine_LoggingBase iff LoggingBase and LoggingFine ;
Derivative_LoggingSevere_LoggingBase iff LoggingBase and LoggingSevere ;
Derivative_LoggingRecovery_LoggingBase iff LoggingBase and LoggingRecovery ;
Derivative_LoggingCleaner_LoggingBase iff LoggingCleaner and LoggingBase ;
Derivative_LoggingFileHandler_LoggingBase iff LoggingBase and LoggingFileHandler ;
Derivative_LoggingDbLogHandler_LoggingBase iff LoggingBase and LoggingDbLogHandler ;
Derivative_LoggingConsoleHandler_LoggingBase iff LoggingBase and LoggingConsoleHandler ;

