export type SingleChooseProblemType = {
    type: 1;
    content: string;
    choices: string[];
    answer: number;
    hint?: string;
};
export type MultiChooseProblemType = {
    type: 2;
    content: string;
    choices: string[];
    answer: number[];
    hint?: string;
};
export type FillingProblemType = {
    type: 3;
    content: string;
    answer: string;
    hint?: string;
};
export type JudgementProblemType = {
    type: 4;
    content: string;
    choices: [string, string];
    answer: number;
    hint?: string;
};
export type ChooseProblemType = SingleChooseProblemType | MultiChooseProblemType | JudgementProblemType;
export type ProblemType = ChooseProblemType | FillingProblemType;
export type ProblemShowType = {
    title: string;
    time: number;
    categories: string[];
    id?: string;
};
