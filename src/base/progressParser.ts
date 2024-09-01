export function parseProgress(data: any) {
    const problemList = data?.problemList;
    const nowProblemId = data?.nowProblemId;
    const problemState = data?.problemState;
    const answerList = data?.answerList;
    if (!problemList || !nowProblemId || !problemState || !answerList) {
        return undefined;
    }
    if (nowProblemId < 0 || nowProblemId >= problemList.length) {
        return undefined;
    }
    if (problemState.length != problemList.length) {
        return undefined;
    }
    if (answerList.length != problemList.length) {
        return undefined;
    }
    for (let i = 0; i < problemList.length; i++) {
        if (problemState[i] !== 0 && problemState[i] !== 1 && problemState[i] !== 2 && problemState[i] !== 3) {
            return undefined;
        }
    }
    return {
        problemList,
        nowProblemId,
        problemState,
        answerList
    };
}