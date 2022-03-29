from typing import Any, BinaryIO, Callable, ClassVar, Dict, Final, List, Optional, Protocol, Sequence, Tuple, Union

NVR = str
NVRA = str  # N-V-R.A
NVR_MAP = Dict[str, str]
NVRA_MAP = Dict[str, Union[bool, str]]
NVRE_MAP = Dict[str, Union[str, int]]

BuildInfo = Dict[str, Any]
RPMInfo = Dict[str, Any]
UserInfo = Dict[str, Any]
TaskRequest = List[Any]
TaskInfo = Dict[str, Any]
BuildTargetInfo = Dict[str, Union[int, str]]

AUTHTYPE_NORMAL: Final[int] = 0
AUTHTYPE_KERB: Final[int] = 1
AUTHTYPE_SSL: Final[int] = 2
AUTHTYPE_GSSAPI: Final[int] = 3

class Enum(dict):
    def __init__(self, *args): ...
    def get(self, key: Union[str, slice], default: Optional[Any] = None) -> Any: ...
    def getnum(self, key: Union[str, slice], default: Optional[Any] = None) -> Any: ...

BUILD_STATES: Enum
TASK_STATES: Enum
USERTYPES: Enum
USER_STATES: Enum

class GenericError(Exception): ...
class ActionNotAllowed(GenericError):
    faultCode: ClassVar[int]

class _TransactionSet(Protocol):
    def setVSFlags(self, flag: int) -> None: ...
    def hdrFromFdno(self, fileno: int) -> Any: ...

def daemonize() -> None: ...
def get_rpm_header(f: Union[str, BinaryIO], ts: Optional[_TransactionSet] = None): ...
def rpm_hdr_size(f: Union[str, BinaryIO], ofs: Optional[int] = None) -> int: ...
def parse_NVR(nvr: str) -> NVR_MAP: ...
def parse_NVRA(nvra: str) -> NVRA_MAP: ...

def read_config(profile_name: str, user_config: Optional[str] = None) -> Dict[str, Union[bool, int, str, None]]: ...
def get_profile_module(profile_name: str, config: Optional[Any] = None) -> Any: ...

class _ConfigParser(Protocol):
    def has_section(self, section_name: str) -> bool: ...
    def items(self, section_name: str) -> Sequence[Tuple[str, Union[int, str]]]: ...
    def getboolean(self, section_name: str, name: str) -> bool: ...

def read_config_files(
    config_files: Union[str, Sequence[str], Sequence[Union[List[Union[bool, str]], Tuple[str, bool]]]], raw: bool = False
): ...

class ClientSession:
    def __init__(
        self,
        baseurl: str,
        opts: Optional[Dict[str, Union[bool, int, str, None]]] = None,
        sinfo: Optional[Dict[str, Union[bool, int, str, None]]] = None,
    ): ...

    # Instance methods
    def ssl_login(
        self,
        cert: Optional[str] = None,
        ca: Optional[str] = None,
        serverca: Optional[str] = None,
        proxyuser: Optional[str] = None,
        proxyauthtype: Optional[str] = None,
    ) -> bool: ...
    def krb_login(
        self,
        principal: Optional[str] = None,
        keytab: Optional[str] = None,
        ccache: Optional[str] = None,
        proxyuser: Optional[str] = None,
        ctx: Optional[Any] = None,
    ) -> bool: ...
    def gssapi_login(
        self,
        principal: Optional[str] = None,
        keytab: Optional[str] = None,
        ccache: Optional[str] = None,
        proxyuser: Optional[str] = None,
        proxyauthtype: Optional[str] = None,
    ) -> bool: ...
    def logout(self) -> None: ...
    def fastUpload(
        self,
        localfile: str,
        path: str,
        name: Optional[str] = None,
        blocksize: Optional[int] = None,
        callback: Optional[Callable[[int, int, int, float, float], None]] = None,
        overwrite: bool = True,
        volume: Optional[str] = None,
    ) -> None: ...
    def uploadWrapper(
        self,
        localfile: str,
        path: str,
        name: Optional[str] = None,
        callback: Optional[Callable[[int, int, int, float, float], None]] = None,
        blocksize: Optional[int] = None,
        overwrite: bool = True,
        volume: Optional[str] = None,
    ) -> None: ...
    def downloadTaskOutput(
        self, taskID: int, fileName: str, offset: int = 0, size: int = -1, volume: Optional[str] = None
    ) -> str: ...

    # Content Generator
    def CGImport(
        self,
        metadata: Union[str, Dict[str, Any]],
        directory: str,
        token: Optional[str] = None,
    ) -> BuildInfo: ...
    def CGInitBuild(self, cg_name: str, data: NVRE_MAP) -> Dict[str, Union[int, str]]: ...
    def CGRefundBuild(self, cg_name: str, build_id: int, token: str, state: int = 3) -> None: ...
    def getNextRelease(self, build_info: Dict[str, str], incr: int = 1) -> str: ...
    def getLatestRPMS(
        self,
        tag: Union[int, str],
        package: Optional[int] = None,
        arch: Optional[Union[str, List[str]]] = None,
        event: Optional[int] = None,
        rpmsigs: bool = False,
        type: Optional[str] = None,
    ) -> Tuple[List[RPMInfo], List[BuildInfo]]: ...
    def getLoggedInUser(self) -> Optional[UserInfo]: ...
    def getUser(
        self,
        userInfo: Optional[Union[int, str, Dict[str, Union[int, str]]]] = None,
        strict: bool = False,
        krb_princs: bool = True,
    ) -> Optional[UserInfo]: ...

    # Build
    def getBuild(self, buildInfo: Union[int, NVR, NVR_MAP], strict: bool = False) -> Optional[BuildInfo]: ...
    def getLatestBuilds(
        self,
        tag: Union[int, str],
        event: Optional[int] = None,
        package: Optional[int] = None,
        type: Optional[str] = None,
    ) -> List[BuildInfo]: ...
    def listBuilds(
        self,
        packageID: Optional[Union[int, str]] = None,
        userID: Optional[Union[int, str]] = None,
        taskID: Optional[int] = None,
        prefix: Optional[str] = None,
        state: Optional[int] = None,
        volumeID: Optional[int] = None,
        source: Optional[str] = None,
        createdBefore: Optional[Union[int, float, str]] = None,
        createdAfter: Optional[Union[int, float, str]] = None,
        completeBefore: Optional[Union[int, float, str]] = None,
        completeAfter: Optional[Union[int, float, str]] = None,
        type: Optional[str] = None,
        typeInfo: Optional[Dict[str, Union[int, str]]] = None,
        queryOpts: Optional[Dict[str, Union[bool, int, str]]] = None,
        pattern: Optional[str] = None,
        cgID: Optional[Union[int, str]] = None,
    ) -> List[BuildInfo]: ...
    def build(
        self,
        src: str,
        target: str,
        opts: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
        channel: Optional[str] = None,
    ) -> int: ...
    def buildContainer(
        self,
        src: str,
        target: str,
        opts: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
        channel: str = "container",
    ) -> int: ...
    def buildSourceContainer(
        self,
        target: str,
        opts: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
        channel: str = "container",
    ): ...
    def cancelBuild(self, buildID: int) -> bool: ...
    def listExternalRepos(
        self,
        info: Optional[Union[int, str]] = None,
        url: Optional[str] = None,
        event: Optional[int] = None,
        queryOpts: Optional[Dict[str, Union[bool, int, str]]] = None,
    ) -> List[Dict[str, Union[int, str]]]: ...

    # Build Target
    def getBuildTarget(
        self, info: Union[int, str], event: Optional[Union[int, str]] = None, strict: bool = False
    ) -> BuildTargetInfo: ...

    # Task
    def getTaskInfo(self, task_id: int, request: bool = False, strict: bool = False) -> TaskInfo: ...
    def getTaskRequest(self, taskId: int) -> TaskRequest: ...
    def getTaskResult(self, taskId: int, raise_fault: bool = True) -> Any: ...
    def taskFinished(self, taskId: int) -> bool: ...
    def cancelTask(self, task_id: int, recurse: bool = True) -> None: ...

    # Package
    def getPackage(
        self, info: Union[int, str], strict: bool = False, create: bool = False
    ) -> Dict[str, Union[int, str]]: ...
    def getPackageID(self, name: str, strict: bool = False) -> int: ...

    # Tag
    def tagBuild(
        self,
        tag: Union[int, str],
        build: Union[int, NVR, NVR_MAP],
        force: bool = False,
        fromtag: Optional[Union[int, str]] = None,
    ) -> int: ...

    # RPM
    def getRPM(
        self, rpminfo: Union[int, str, Dict[str, str]], strict: bool = False, multi: bool = False
    ) -> RPMInfo: ...
