#ifndef H_LinuxCommon
#define H_LinuxCommon

#include <sys/types.h>

/* Common typedefs for Linux */

typedef unsigned char *			StringPtr;
typedef unsigned char			Boolean;
typedef char *				Ptr;

typedef unsigned char			UInt8;
typedef UInt8*				PUInt8;
typedef signed char			SInt8;
typedef unsigned short			UInt16;
typedef signed short			SInt16;
typedef u_int32_t			UInt32;
typedef int32_t				SInt32;
//typedef unsigned long			UInt32;
//typedef signed long			SInt32;
typedef __S64_TYPE			SInt64;
typedef __U64_TYPE			UInt64;
typedef __S64_TYPE			int64_t;
typedef __U64_TYPE			uint64_t;

//typedef unsigned long	ULONG;
//typedef void*			LPVOID;
//typedef	long			HRESULT;
//typedef	int32_t			HRESULT;

typedef SInt16				OSErr;

typedef unsigned long			FourCharCode;
typedef FourCharCode			OSType;

typedef void IUnknown;

#define FAILED(Status)		((HRESULT)(Status) < 0)

/* dummy definitions - TODO: define these ... or not? */

typedef int	FSSpec;
typedef int	CFURLRef;
typedef int	CFBundleRef;
typedef void*				Handle;   // needed by Python driver

/* re-define MAC-only memory API to POSIX-compliant */
#define NewPtr		malloc	/* MAC */
#define DisposePtr	free	/* MAC */

/* re-define WinDoze-only memory API to POSIX-compliant */
/* currently not used because we are using #ifdef __MAC__ */

// #define CoTaskMemAlloc		malloc
// #define CoTaskMemFree		free
// #define CoTaskMemRealloc	realloc


#endif /* H_LinuxCommon */

